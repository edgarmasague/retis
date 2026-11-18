"""
Basic configuration generator for Retis.

This module implements the generator responsible for creating the
initial and general configuration settings shared by Cisco routers
and switches.

It provides the functionality required to configure common device
parameters, ensuring that essential settings are applied consistently
regardless of the network device type.

The generator collects and validates the required user input and
uses the corresponding configuration template to produce the
appropriate Cisco IOS commands.

Its purpose is to establish a common configuration baseline for
network devices before applying more specific settings such as
interfaces, routing, VLANs or security.

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


class BasicGenerator(TemplateGenerator):
    """Hostname, domain name and optional MOTD banner."""

    def __init__(self) -> None:
        super().__init__(
            "common/basic.cfg",
            (
                Parameter("hostname", validators.hostname),
                Parameter("domain", validators.domain),
                Parameter("banner", validators.banner, optional=True),
            ),
        )
