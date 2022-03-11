'''
Update all the user configuration in this file
'''

# configure colors in this class
class nonpowershell():
    """
    Colorscheme for terminal emulators other than default powershell in windows,
    Contains dark blue for style coloring.
    """

    #Foreground Colors
    FALERT   : str = "red"
    FSUCCESS : str = "green"
    FURGENT  : str = "yellow"
    FPROMPT  : str = "blue"

    #Background Colors
    BALERT   : str = "bold white on red"
    BSUCCESS : str = "bold white on green"
    BURGENT  : str = "bold black on yellow"


class powershell():
    """
    Colorscheme for the default powershell in windows,
    Contains lighter shade of blue (cyan) for more visible style coloring
    """

    #Foreground Colors
    FALERT   : str = "red"
    FSUCCESS : str = "green"
    FURGENT  : str = "yellow"
    FPROMPT  : str = "cyan"

    #Background Colors
    BALERT   : str = "bold white on red"
    BSUCCESS : str = "bold white on green"
    BURGENT  : str = "bold black on yellow"

# Chose color scheme(light or dark)
colors = nonpowershell

#Assign what module to use at startup
MODULE = ""

#Assign values to options at startup
OPTIONS = {
    "thost": "127.0.0.1",
    "tport": "",
    "protocol": "",
    "verbose": "",
    "turl": "https://www.example.com",
}

# Aliases for the user's comfort
aliases : dict = {
    'execute': 'run',
    'info': 'show info',
    'options': 'show options'
}

macros: dict = {
    'localhost': '127.0.0.1',
    'example': 'https://www.example.com',
}
