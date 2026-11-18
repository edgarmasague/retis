"""
Interactive command-line interface for Retis.

This module provides the user interface for interacting with the
Retis application through a terminal environment.

It manages the interaction between the user and the configuration
generation system, allowing users to select network devices, choose
configuration sections, provide the required input values and
generate Cisco IOS configuration scripts.

The interface also handles navigation through the available menus,
user input processing and actions such as undoing the last added
configuration section.

It acts as the main entry point for user interaction with the
application.

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""

import os

from retis.core.engine import ConfigurationEngine
from retis.utils.files import FileManager


class CLI:
    """Manage the interactive Retis command-line interface."""

    MENUS = {
        "router": {
            "1": ("Basic configuration", "basic"),
            "2": ("Interface configuration", "interfaces"),
            "3": ("Static routing", "routing"),
            "4": ("Security configuration", "security"),
        },
        "switch": {
            "1": ("Basic configuration", "basic"),
            "2": ("VLAN configuration", "vlan"),
            "3": ("Security configuration", "security"),
        },
    }

    def __init__(
        self,
        engine: ConfigurationEngine,
        file_manager: FileManager,
    ) -> None:
        """Initialize CLI dependencies."""
        self.engine = engine
        self.file_manager = file_manager
        self.current_filename: str | None = None
        self.current_extension = ".txt"
        self.sections: list[str] = []

    @staticmethod
    def _clear_screen() -> None:
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def _header(title: str) -> None:
        """Display a formatted menu header."""
        print("\n" + "=" * 45)
        print(f" {title}")
        print("=" * 45)

    @staticmethod
    def _ask(prompt: str) -> str:
        """Ask the user for a value."""
        return input(f"{prompt}: ").strip()

    def _select_output_file(self) -> bool:
        """Ask for the output filename and extension."""
        self._header("OUTPUT FILE")

        filename = self._ask("Enter configuration filename")

        if not filename:
            print("Filename cannot be empty.")
            return False

        try:
            path = self.file_manager.resolve(filename, self.current_extension)
            exists = path.exists()
        except ValueError as error:
            print(f"Invalid filename: {error}")
            return False

        if exists:
            answer = self._ask(f"{path.name} already exists. Overwrite? (y/N)")
            if answer.lower() not in ("y", "yes", "s", "si", "sí"):
                return False

        self.current_filename = filename
        return True

    def _device_menu(self, device_type: str) -> None:
        """Display the configuration menu for a device."""
        options = self.MENUS[device_type]

        if not self._select_output_file():
            input("\nPress ENTER to continue...")
            return

        while True:
            self._clear_screen()
            self._header(f"{device_type.upper()} CONFIGURATION")

            print(f"Output file: {self.current_filename}"
                  f"{self.current_extension}")
            print(f"Sections in script: {len(self.sections)}\n")

            for key, (description, _) in options.items():
                print(f"{key}. {description}")

            print("U. Undo last section")
            print("0. Back")

            choice = self._ask("Select an option").lower()

            if choice == "0":
                self.current_filename = None
                self.sections = []
                return

            if choice == "u":
                self._undo()
            elif choice in options:
                self._generate(device_type, options[choice][1])
            else:
                print("Invalid option.")

            input("\nPress ENTER to continue...")

    def _generate(
        self,
        device_type: str,
        config_type: str,
    ) -> None:
        """Collect parameters, generate a section and rewrite the file."""
        try:
            generator = self.engine.get_generator(device_type, config_type)

            self._clear_screen()
            self._header("CONFIGURATION PARAMETERS")

            values = {
                parameter.name: self._ask(parameter.label)
                for parameter in generator.parameters
            }

            section = self.engine.generate(device_type, config_type, values)

        except ValueError as error:
            print(f"\nError: {error}")
            return

        self.sections.append(section)

        try:
            self._write()
        except (OSError, ValueError) as error:
            self.sections.pop()
            print(f"\nCould not save configuration: {error}")

    def _undo(self) -> None:
        """Remove the last section and rewrite (or delete) the file."""
        if not self.sections:
            print("\nNothing to undo.")
            return

        self.sections.pop()

        try:
            if self.sections:
                self._write()
            else:
                self.file_manager.remove(
                    self.current_filename, self.current_extension
                )
                print("\nScript is empty; output file removed.")
        except (OSError, ValueError) as error:
            print(f"\nCould not update file: {error}")

    def _write(self) -> None:
        """Assemble all sections into one script and save it."""
        script = self.engine.assemble(self.sections)

        path = self.file_manager.save(
            script,
            self.current_filename,
            self.current_extension,
        )

        self._clear_screen()
        self._header("CURRENT SCRIPT")
        print(script)
        print(f"Script saved to: {path}")

    def run(self) -> None:
        """Start the main interactive menu."""
        while True:
            self._clear_screen()
            self._header("RETIS - CISCO IOS CONFIGURATION GENERATOR")

            print("1. Router")
            print("2. Switch")
            print("0. Exit")

            choice = self._ask("Select an option")

            if choice == "1":
                self._device_menu("router")

            elif choice == "2":
                self._device_menu("switch")

            elif choice == "0":
                self._clear_screen()
                print("Thank you for using RETIS!")
                return

            else:
                print("Invalid option.")
                input("\nPress ENTER to continue...")
