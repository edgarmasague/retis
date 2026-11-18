"""
Static routing configuration generator for Retis.

This module implements the generator responsible for creating
Cisco IOS commands to configure static routes on network devices.

It provides the functionality required to define routing entries
that specify how network traffic should be forwarded towards
remote destination networks.

The generator collects and validates the required routing
information, such as destination network addresses, subnet masks
and next-hop addresses or exit interfaces, depending on the
supported configuration options.

It then processes the provided parameters and uses the appropriate
configuration template to generate the corresponding Cisco IOS
static routing commands.

Static routing allows network administrators to manually define
the paths used by devices to reach networks that are not directly
connected, providing control over traffic forwarding.

The generated configuration section is integrated into the final
script by the Retis configuration engine.

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""

import ipaddress

from retis.generators.base import Parameter, TemplateGenerator
from retis.utils import validators
from retis.utils.validators import ValidationError


class StaticRoutingGenerator(TemplateGenerator):
    """Generate static routes for a router."""

    def __init__(self) -> None:
        super().__init__(
            "router/routing.cfg",
            (
                Parameter("network", validators.ipv4),
                Parameter("subnet_mask", validators.netmask),
                Parameter("next_hop", validators.ipv4),
            ),
        )

    def check(self, values: dict[str, str]) -> None:
        """Ensure the network address matches its mask."""
        try:
            ipaddress.IPv4Network(
                f"{values['network']}/{values['subnet_mask']}"
            )
        except ValueError:
            raise ValidationError(
                f"{values['network']} {values['subnet_mask']} is "
                "inconsistent: the network address has host bits set."
            ) from None
