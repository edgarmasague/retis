"""
Input validation utilities for Retis.

This module provides validation functions for network-related
parameters entered by users through the interactive command-line
interface.

It ensures that the supplied values follow the expected formats
and constraints before they are used to generate Cisco IOS
configuration commands.

The validation functions cover different types of network
parameters, helping prevent invalid or inconsistent configuration
values from being included in the generated scripts.

Each validator follows a consistent interface and either returns
the normalized value when validation succeeds or raises a
ValidationError when the provided input is invalid.

Returning normalized values ensures that validated parameters
are represented consistently throughout the application.

These functions are shared by the different configuration
generators to centralize validation logic and avoid code
duplication.

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""

import ipaddress
import re


class ValidationError(ValueError):
    """Raised when a user-supplied value is not valid."""


_INTERFACE_TYPES = (
    "Ethernet",
    "FastEthernet",
    "GigabitEthernet",
    "TenGigabitEthernet",
    "Serial",
    "Loopback",
    "Vlan",
)
_INTERFACE_RE = re.compile(r"([A-Za-z]+)\s*(\d+(?:/\d+){0,3}(?:\.\d+)?)")
_HOSTNAME_RE = re.compile(r"[A-Za-z](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")
_LABEL_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")
_VLAN_NAME_RE = re.compile(r"[A-Za-z0-9_-]{1,32}")


def hostname(value: str) -> str:
    """Validate an IOS hostname."""
    if not _HOSTNAME_RE.fullmatch(value):
        raise ValidationError(
            "Hostname must start with a letter, contain only letters, "
            "digits or hyphens, and end with a letter or digit (max 63)."
        )
    return value


def domain(value: str) -> str:
    """Validate a DNS domain name (an IP address is not a domain)."""
    try:
        ipaddress.ip_address(value)
    except ValueError:
        pass
    else:
        raise ValidationError("A domain name cannot be an IP address.")

    labels = value.split(".")
    if len(value) > 253 or not all(_LABEL_RE.fullmatch(lab) for lab in labels):
        raise ValidationError("Invalid domain name (example: lab.local).")
    return value


def ipv4(value: str) -> str:
    """Validate an IPv4 address."""
    try:
        return str(ipaddress.IPv4Address(value))
    except ValueError:
        raise ValidationError(
            f"'{value}' is not a valid IPv4 address."
        ) from None


def netmask(value: str) -> str:
    """Validate a subnet mask (dotted or /prefix) and return it dotted."""
    raw = value.lstrip("/")

    if raw.isascii() and raw.isdigit():
        prefix = int(raw)
        if not 0 <= prefix <= 32:
            raise ValidationError("Prefix length must be between 0 and 32.")
        bits = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        return str(ipaddress.IPv4Address(bits))

    try:
        bits = int(ipaddress.IPv4Address(raw))
    except ValueError:
        raise ValidationError(
            f"'{value}' is not a valid subnet mask (e.g. 255.255.255.0 or /24)."
        ) from None

    inverse = bits ^ 0xFFFFFFFF
    if inverse & (inverse + 1):
        raise ValidationError(f"'{value}' is not a contiguous subnet mask.")
    return raw


def interface(value: str) -> str:
    """Validate an interface name and expand abbreviations (g0/1 -> ...)."""
    match = _INTERFACE_RE.fullmatch(value.strip())
    if not match:
        raise ValidationError(
            "Invalid interface (example: GigabitEthernet0/1 or g0/1)."
        )

    prefix, numbers = match.group(1).lower(), match.group(2)
    candidates = [
        name for name in _INTERFACE_TYPES if name.lower().startswith(prefix)
    ]
    if len(candidates) != 1:
        raise ValidationError(
            f"Unknown or ambiguous interface type '{match.group(1)}'."
        )
    return f"{candidates[0]}{numbers}"


def vlan_id(value: str) -> str:
    """Validate a VLAN ID."""
    if not (value.isascii() and value.isdigit()) or not 1 <= int(value) <= 4094:
        raise ValidationError("VLAN ID must be a number between 1 and 4094.")
    if 1002 <= int(value) <= 1005:
        raise ValidationError("VLAN IDs 1002-1005 are reserved.")
    return str(int(value))


def vlan_name(value: str) -> str:
    """Validate a VLAN name."""
    if not _VLAN_NAME_RE.fullmatch(value):
        raise ValidationError(
            "VLAN name: 1-32 letters, digits, '_' or '-', no spaces."
        )
    return value


def password(value: str) -> str:
    """Validate a password or secret."""
    if any(char.isspace() for char in value):
        raise ValidationError("Passwords cannot contain spaces.")
    return value


def banner(value: str) -> str:
    """Validate a MOTD banner (uses '#' as delimiter)."""
    if "#" in value:
        raise ValidationError("The banner cannot contain '#'.")
    return value


def description(value: str) -> str:
    """Validate an interface description."""
    if len(value) > 200:
        raise ValidationError("Description is limited to 200 characters.")
    return value
