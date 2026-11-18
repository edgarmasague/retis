"""
VLAN configuration generator for Retis.

This module implements the generator responsible for creating
Cisco IOS configuration commands for Virtual Local Area Networks
(VLANs) on supported network devices.

It provides the functionality required to create and configure
VLANs, allowing network administrators to logically segment a
physical network into separate broadcast domains.

The generator collects and validates the required user input,
such as VLAN identifiers and names, before processing the
configuration parameters.

It then uses the appropriate configuration template to generate
the corresponding Cisco IOS commands for VLAN creation and
management.

VLAN configuration helps improve network organization, traffic
segmentation and network administration by separating devices
into logical network groups.

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

from retis.generators.base import Parameter, TemplateGenerator
from retis.utils import validators


class VLANGenerator(TemplateGenerator):
    """Generate VLAN configuration for a switch."""

    def __init__(self) -> None:
        super().__init__(
            "switch/vlan.cfg",
            (
                Parameter("vlan_id", validators.vlan_id),
                Parameter("vlan_name", validators.vlan_name),
            ),
        )
