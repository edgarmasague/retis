"""
Configuration generation engine for Retis.

This module implements the core logic responsible for managing and
coordinating the configuration generation process.

It handles the registration and execution of configuration generators,
ensuring that each generator is properly integrated into the application
and can produce its corresponding Cisco IOS configuration section.

The engine is responsible for collecting the generated configuration
sections, maintaining their execution order and combining them into
a complete configuration script.

It also manages the overall generation workflow, ensuring that the
resulting script follows the expected structure and can be exported
as a configuration file.

This module acts as the central connection between the application's
command-line interface and its configuration generators.

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""

from collections.abc import Mapping, Sequence

from retis.generators.base import BaseGenerator
from retis.generators.basic import BasicGenerator
from retis.generators.interfaces import InterfaceGenerator
from retis.generators.routing import StaticRoutingGenerator
from retis.generators.security import SecurityGenerator
from retis.generators.vlan import VLANGenerator


class ConfigurationEngine:
    """Coordinate Cisco IOS configuration generators."""

    HEADER = ("configure terminal",)
    FOOTER = ("end", "copy running-config startup-config")

    def __init__(self) -> None:
        """Register all available generators."""
        basic = BasicGenerator()
        security = SecurityGenerator()

        self._generators: dict[tuple[str, str], BaseGenerator] = {
            ("router", "basic"): basic,
            ("router", "interfaces"): InterfaceGenerator(),
            ("router", "routing"): StaticRoutingGenerator(),
            ("router", "security"): security,
            ("switch", "basic"): basic,
            ("switch", "vlan"): VLANGenerator(),
            ("switch", "security"): security,
        }

    def get_generator(
        self,
        device_type: str,
        config_type: str,
    ) -> BaseGenerator:
        """Return the requested generator."""
        key = (device_type.lower(), config_type.lower())

        if key not in self._generators:
            raise ValueError(
                f"Unsupported configuration: {device_type}/{config_type}"
            )

        return self._generators[key]

    def generate(
        self,
        device_type: str,
        config_type: str,
        parameters: Mapping[str, str],
    ) -> str:
        """
        Generate one configuration section (lines only, no wrapper).

        Raises:
            ValueError: Unsupported configuration or invalid parameters.
        """
        generator = self.get_generator(device_type, config_type)
        return generator.generate(parameters)

    def assemble(self, sections: Sequence[str]) -> str:
        """Join sections into one script wrapped exactly once."""
        lines = [*self.HEADER, *sections, *self.FOOTER]
        return "\n".join(lines) + "\n"
