"""
Basic device security generator for Retis.

This module implements the generator responsible for creating
basic security configuration commands shared by Cisco routers
and switches.

It provides the functionality required to configure common
device security settings, helping protect network devices against
unauthorized access and improving the overall security of the
network infrastructure.

The generator collects and validates the required security-related
user input and processes the selected options to produce the
corresponding Cisco IOS configuration commands.

Depending on the supported configuration options, these settings
may include password protection, access control, authentication
and other basic device security mechanisms.

The generator uses the appropriate configuration template to
maintain consistency and structure in the generated commands.

The resulting configuration section is integrated into the final
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


class SecurityGenerator(TemplateGenerator):
    """Enable secret, console and VTY access, password encryption."""

    def __init__(self) -> None:
        super().__init__(
            "common/security.cfg",
            (
                Parameter("enable_secret", validators.password, secret=True),
                Parameter("console_password", validators.password, secret=True),
                Parameter("vty_password", validators.password, secret=True),
            ),
        )
