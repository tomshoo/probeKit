"""
Update all the user configuration in this file
"""


# configure colors in this class
class NonWindows10PowerShell:
    """
    Colorscheme for terminal emulators other than default powershell in windows,
    Contains dark blue for style coloring.
    """

    # Foreground Colors
    FALERT: str = "red"
    FSUCCESS: str = "green"
    FURGENT: str = "yellow"
    FPROMPT: str = "blue"

    # Background Colors
    BALERT: str = "bold white on red"
    BSUCCESS: str = "bold white on green"
    BURGENT: str = "bold black on yellow"


class Windows10PowerShell:
    """
    Colorscheme for the default powershell in windows,
    Contains lighter shade of blue (cyan) for more visible style coloring
    """

    # Foreground Colors
    FALERT: str = "red"
    FSUCCESS: str = "green"
    FURGENT: str = "yellow"
    FPROMPT: str = "cyan"

    # Background Colors
    BALERT: str = "bold white on red"
    BSUCCESS: str = "bold white on green"
    BURGENT: str = "bold black on yellow"


# Chose color scheme(for Windows 10 powershell or otherwise)
colors = NonWindows10PowerShell

# Assign what module to use at startup
MODULE: str = ""

# Assign values to options at startup
OPTIONS: dict[str, str] = {
    "thost": "127.0.0.1",
    "tport": "",
    "protocol": "",
    "verbose": "",
    "turl": "https://www.example.com",
}

# Default command header,#
# in case the user set aliases with names of default commands,
# and is later unable to use the original command.
# This same command would then be accessible by <default_command_header.command>
default_command_header: str = "self"

# Aliases for the user's comfort
user_aliases: dict[str, str] = {
    "execute": "run",
    "info": "show info",
    "options": "show options",
}

macros: dict[str, str] = {
    "localhost": "127.0.0.1",
    "example": "https://www.example.com",
}
