import json
from os import path
from platform import platform
from colorama import Fore, Back

# configure colors in this class
class nonpowershell():
    #Foreground Colors
    FALERT   : str = Fore.RED
    FSUCCESS : str = Fore.GREEN
    FNORMAL  : str = Fore.RESET
    FURGENT  : str = Fore.YELLOW
    FPROMPT  : str = Fore.BLUE

    #Background Colors
    BALERT   : str = Back.RED
    BSUCCESS : str = Back.GREEN
    BNORMAL  : str = Back.RESET
    BURGENT  : str = Back.YELLOW


class powershell():
    #Foreground Colors
    FALERT   : str = Fore.RED
    FSUCCESS : str = Fore.GREEN
    FNORMAL  : str = Fore.RESET
    FURGENT  : str = Fore.YELLOW
    FPROMPT  : str = Fore.CYAN

    #Background Colors
    BALERT   : str = Back.RED
    BSUCCESS : str = Back.GREEN
    BNORMAL  : str = Back.RESET
    BURGENT  : str = Back.YELLOW

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

#Read the config.json file
if 'Windows' in platform():
    data_path = path.expanduser('~\\Documents\\probeKit\\config.json')
else:
    data_path = path.expanduser('~/.config/probekit/config.json')

with open(data_path, 'r') as f:
    data_str = f.read()
data = json.loads(data_str)

#List valid modules from config.json
valid_modules: dict = data['modules']

#Read the rules for valid options
option_dict: dict = data['options']

#Override options with values provided by the user
for option in option_dict:
    if OPTIONS.get(option):
        if option_dict[option]['type'] == "dict":
            option_dict[option]['value']['value'] = OPTIONS.get(option)
        else:
            option_dict[option]['value'] = OPTIONS.get(option)

# Aliases for the user's comfort
aliases : dict = {
    'execute': 'run',
    'info': 'show info',
    'options': 'show options',
}
