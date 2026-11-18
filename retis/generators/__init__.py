"""
Cisco IOS configuration generators for Retis.

This package contains the generator modules responsible for creating
Cisco IOS configuration commands for different network device settings.

Each generator focuses on a specific configuration area and provides
the logic required to collect, validate and process user input before
producing the corresponding configuration commands.

The available configuration categories include:

    - Basic: General device settings and initial configuration.
    - Interfaces: Physical and logical network interface configuration.
    - Routing: Routing protocols and static route configuration.
    - VLAN: Virtual LAN creation and management.
    - Security: Device access control and security settings.

Generators use predefined configuration templates to ensure
consistency, readability and maintainability across the generated
scripts.

The generated sections are integrated by the core engine into a
complete Cisco IOS configuration script.

Attributes:
    __author__ (str): Edgar Masague.
    __version__ (str): 0.1.0.
    __project__ (str): Retis.
    __license__ (str): MIT License.
    __maintainer__ (str): Edgar Masague.
    __status__ (str): Development.
"""