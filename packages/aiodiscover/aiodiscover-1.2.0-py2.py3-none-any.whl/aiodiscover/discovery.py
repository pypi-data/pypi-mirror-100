import asyncio
from contextlib import suppress
import logging

from async_dns import DNSMessage, types
from async_dns.resolver import ProxyResolver
from pyroute2 import IPRoute

from .network import SystemNetworkData
from .utils import CONCURRENCY_LIMIT, gather_with_concurrency

HOSTNAME = "hostname"
MAC_ADDRESS = "macaddress"
IP_ADDRESS = "ip"
MAX_ADDRESSES = 2048

_LOGGER = logging.getLogger(__name__)


def ip_to_ptr(ip_address):
    """Convert an ip string to a PTR."""
    ipl = ip_address.split(".")
    ipl.reverse()
    return f"{'.'.join(ipl)}.in-addr.arpa"


def short_hostname(hostname):
    """The first part of the hostname."""
    return hostname.split(".")[0]


def dns_message_short_hostname(dns_message):
    """Get the short hostname from a dns message."""
    if not isinstance(dns_message, DNSMessage):
        return None
    record = dns_message.get_record((types.PTR,))
    if record is None:
        return None
    return short_hostname(record)


async def async_query_for_ptrs(resolver, ips_to_lookup):
    """Fetch PTR records for a list of ips."""
    return await gather_with_concurrency(
        CONCURRENCY_LIMIT,
        *[
            resolver.query(ip_to_ptr(str(ip)), qtype=types.PTR, timeout=2.0)
            for ip in ips_to_lookup
        ],
        return_exceptions=True,
    )


class DiscoverHosts:
    """Discover hosts on the network by ARP and PTR lookup."""

    def __init__(self):
        """Init the discovery hosts."""
        self.ip_route = None
        with suppress(Exception):
            self.ip_route = IPRoute()

    async def async_discover(self):
        """Discover hosts on the network by ARP and PTR lookup."""
        sys_network_data = SystemNetworkData(self.ip_route)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sys_network_data.setup)
        hostnames = await self.async_get_hostnames(sys_network_data)
        neighbours = await sys_network_data.async_get_neighbors(hostnames.keys())
        return [
            {
                HOSTNAME: hostname,
                MAC_ADDRESS: neighbours[ip],
                IP_ADDRESS: ip,
            }
            for ip, hostname in hostnames.items()
            if ip in neighbours
        ]

    async def _async_get_nameservers(self, sys_network_data):
        """Get nameservers to query."""
        all_nameservers = list(sys_network_data.nameservers)
        router_ip = sys_network_data.router_ip
        if router_ip not in all_nameservers:
            neighbours = await sys_network_data.async_get_neighbors([router_ip])
            if router_ip in neighbours:
                all_nameservers.insert(0, router_ip)
        return all_nameservers

    async def async_get_hostnames(self, sys_network_data):
        """Lookup PTR records for all addresses in the network."""
        all_nameservers = await self._async_get_nameservers(sys_network_data)
        ips = []
        for host in sys_network_data.network.hosts():
            if len(ips) > MAX_ADDRESSES:
                _LOGGER.warning(
                    "Max addresses of %s reached for network: %s",
                    MAX_ADDRESSES,
                    sys_network_data.network,
                )
                break
            ips.append(str(host))

        hostnames = {}
        for nameserver in all_nameservers:
            ips_to_lookup = [ip for ip in ips if ip not in hostnames]
            results = await async_query_for_ptrs(
                ProxyResolver(proxies=[nameserver]), ips_to_lookup
            )
            for idx, ip in enumerate(ips_to_lookup):
                short_host = dns_message_short_hostname(results[idx])
                if short_host is None:
                    continue
                hostnames[ip] = short_host
            if hostnames:
                # As soon as we have a responsive nameserver, there
                # is no need to query additional fallbacks
                break
        return hostnames
