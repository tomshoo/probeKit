import json
from os import path
from pathlib import Path

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

#############################NOTE#############################
# Everything after this point is used to process all the     #
# configuration provided by the user.                        #
# Editing anything after this point may tend to break stuff. #
# Edit anything only if absolutely neccessary, and you know  #
# what exactly you want to achieve                           #
##############################################################

#Read the config.json file
data_path = Path(__file__).parent
data_path = path.join(data_path, 'config.json')
with open(data_path, 'r') as f: data_str = f.read()
data = json.loads(data_str)

#List valid modules from config.json
valid_modules: dict = data['modules']

#Read the rules for valid options
option_dict: dict = data['options']

#Override options with values provided by the user
for option in option_dict:
    if OPTIONS.get(option):
        if option_dict[option]['type'] == "dict": option_dict[option]['value']['value'] = OPTIONS.get(option)
        else: option_dict[option]['value'] = OPTIONS.get(option)