"""
Retis - Modular Network Generator.

Retis is an interactive Python application designed to simplify
the generation of Cisco IOS configuration scripts for network
devices, including routers and switches.

The application provides a modular and extensible architecture
that allows users to generate configuration commands through
an interactive command-line interface.

It organizes configuration tasks into independent sections,
allowing users to configure different aspects of network devices,
including:

    - Basic device configuration.
    - Network interface configuration.
    - Static routing configuration.
    - Virtual Local Area Network (VLAN) configuration.
    - Basic device security configuration.

Each configuration section is handled by a dedicated generator
that processes user input, validates configuration parameters
and uses predefined templates to produce Cisco IOS commands.

The generated sections are assembled into a complete configuration
script, which can be exported to a text file for deployment on
compatible Cisco network devices.

Retis follows a modular design that promotes code reuse,
maintainability and extensibility, making it easier to introduce
additional configuration features and device capabilities.

Package structure:
    core:
        Application engine, generator registry and command-line
        interface.

    generators:
        Specialized modules for generating Cisco IOS configuration
        sections.

    templates:
        Predefined configuration templates used by the generators.

    utils:
        Shared utilities for input validation and file management.

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""
__version__ = "0.1.0"
