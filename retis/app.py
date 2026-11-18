"""
Main application module for Retis.

This module serves as the primary entry point for starting the
Retis application and coordinating its execution workflow.

It initializes the application and delegates control to the
appropriate components responsible for handling user interaction
and configuration script generation.

The module connects the application's startup process with the
interactive command-line interface, allowing users to access
the available configuration generators and build Cisco IOS
configuration scripts for routers and switches.

It ensures that the necessary application components are
invoked in the appropriate order to provide a consistent
execution flow.

This module can be used as the main starting point when
launching Retis through its configured application entry point.

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""

from retis.core.cli import CLI
from retis.core.engine import ConfigurationEngine
from retis.utils.files import FileManager


class RETIS:
    """Main application controller."""

    def __init__(self) -> None:
        """Initialize RETIS and its components."""
        self.engine = ConfigurationEngine()
        self.file_manager = FileManager()
        self.cli = CLI(self.engine, self.file_manager)

    def run(self) -> None:
        """Start the interactive application."""
        self.cli.run()


def main() -> None:
    """Application entry point."""
    try:
        application = RETIS()
        application.run()
    except (KeyboardInterrupt, EOFError):
        print("\nRETIS interrupted. Goodbye!")
