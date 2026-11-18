"""
Retis module execution entry point.

This module enables Retis to be executed directly as a Python
module using the standard Python module execution mechanism.

When invoked with the -m flag, Python executes this module,
allowing the application to start without requiring users to
specify the location of the main script.

It delegates the application startup process to the appropriate
entry point, typically the command-line interface, ensuring that
the interactive Retis environment is launched correctly.

This provides an alternative execution method alongside the
console script installed through Poetry.

Usage:
    poetry run python -m retis

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""

from retis.app import main
if __main__ == "__main__":
    main()
