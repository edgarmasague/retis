"""
Network interface configuration generator for Retis.

This module implements the generator responsible for creating
Cisco IOS configuration commands for network interfaces.

It provides the functionality required to configure physical and
logical interfaces on supported network devices, allowing users
to define interface parameters according to their network
requirements.

The generator collects and validates the necessary user input,
processes the selected interface settings and uses the appropriate
configuration template to generate the corresponding Cisco IOS
commands.

Depending on the supported configuration options, this may include
interface identification, IP addressing, subnet masks, descriptions,
administrative status and other interface-related parameters.

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


class InterfaceGenerator(TemplateGenerator):
    """Generate router interface configuration."""

    def __init__(self) -> None:
        super().__init__(
            "router/interfaces.cfg",
            (
                Parameter("interface", validators.interface),
                Parameter("ip_address", validators.ipv4),
                Parameter("subnet_mask", validators.netmask),
                Parameter(
                    "description", validators.description, optional=True
                ),
            ),
        )

    def check(self, values: dict[str, str]) -> None:
        """Reject the network and broadcast address as interface IP."""
        iface = ipaddress.IPv4Interface(
            f"{values['ip_address']}/{values['subnet_mask']}"
        )
        network = iface.network

        if network.prefixlen < 31 and iface.ip in (
            network.network_address,
            network.broadcast_address,
        ):
            raise ValidationError(
                "The IP address cannot be the network or broadcast "
                "address of its subnet."
            )
