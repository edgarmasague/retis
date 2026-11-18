"""
Base classes for configuration generators in Retis.

This module defines the foundational classes used by the different
Cisco IOS configuration generators.

It provides a common structure and shared functionality that can be
inherited by specialized generators, promoting code reuse, consistency
and maintainability throughout the application.

The base classes establish the common interface and expected
behaviour for configuration generators, allowing individual
implementations to focus on specific network configuration areas
such as basic settings, interfaces, routing, VLANs and security.

These classes help standardize the configuration generation workflow
and ensure compatibility with the core engine.

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""

import re
from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from string import Template

from retis.utils.validators import ValidationError

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_PLACEHOLDER = re.compile(r"\$(\w+)")

Validator = Callable[[str], str]


def _identity(value: str) -> str:
    return value


@dataclass(frozen=True)
class Parameter:
    """Describe one value a generator needs from the user."""

    name: str
    validator: Validator = _identity
    secret: bool = False
    optional: bool = False

    @property
    def label(self) -> str:
        """Human-readable name used in prompts."""
        return self.name.replace("_", " ").capitalize()

    def clean(self, raw: str) -> str:
        """Strip and validate a raw value; empty is allowed if optional."""
        value = raw.strip()

        if not value:
            if self.optional:
                return ""
            raise ValidationError(f"{self.label} cannot be empty.")

        return self.validator(value)


class BaseGenerator(ABC):
    """Abstract base class for Cisco IOS configuration generators.

    Generators return only the configuration lines of their section.
    The engine adds `configure terminal`, `end` and the save command once.
    """

    @property
    @abstractmethod
    def parameters(self) -> tuple[Parameter, ...]:
        """Return the parameters required by the generator."""
        raise NotImplementedError

    def check(self, values: dict[str, str]) -> None:
        """Validate relations between parameters (override if needed)."""

    @abstractmethod
    def render(self, values: dict[str, str]) -> str:
        """Render configuration lines from already-validated values."""
        raise NotImplementedError

    def generate(self, raw: Mapping[str, str]) -> str:
        """Validate raw input and return the configuration lines."""
        values = {
            parameter.name: parameter.clean(raw.get(parameter.name, ""))
            for parameter in self.parameters
        }
        self.check(values)
        return self.render(values)


class TemplateGenerator(BaseGenerator):
    """Generator that fills a `string.Template` file from templates/.

    A template line is skipped when any of its placeholders is empty,
    which is how optional parameters (banner, description) disappear.
    """

    def __init__(
        self,
        template: str,
        parameters: tuple[Parameter, ...],
    ) -> None:
        self._template = template
        self._parameters = parameters

    @property
    def parameters(self) -> tuple[Parameter, ...]:
        return self._parameters

    def render(self, values: dict[str, str]) -> str:
        text = (TEMPLATES_DIR / self._template).read_text(encoding="utf-8")
        lines = []

        for line in text.splitlines():
            names = _PLACEHOLDER.findall(line)

            for name in names:
                if name not in values:
                    raise ValueError(
                        f"Template '{self._template}' uses unknown "
                        f"parameter '{name}'."
                    )

            if any(not values[name] for name in names):
                continue

            lines.append(Template(line).substitute(values))

        return "\n".join(lines)
