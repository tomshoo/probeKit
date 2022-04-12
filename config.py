'''
***************************NOTE*****************************

# Everything after this point is used to process all the
# configuration provided by the user.
# Editing anything after this point may tend to break stuff.
# Edit anything only if absolutely neccessary, and you know 
# what exactly you want to achieve

************************************************************
'''

import json
from os import path
from pathlib import Path
from UserConfig import *

#Read the config.json file
data_path = Path(__file__).parent
data_path = path.join(data_path, 'config.json')
with open(data_path, 'r') as f: data_str = f.read()
data = json.loads(data_str)

default_command_dict: dict[str, list[str, bool]] = {    
    # Default aliases
    'back':   [f'{default_command_header}.back',   True],
    'banner': [f'{default_command_header}.banner', True],
    'clear':  [f'{default_command_header}.clear',  True],
    'doc':    [f'{default_command_header}.doc',    True],
    'help':   [f'{default_command_header}.help',   True],
    'run':    [f'{default_command_header}.run',    True],
    'set':    [f'{default_command_header}.set',    True],
    'show':   [f'{default_command_header}.show',   True],
    'unset':  [f'{default_command_header}.unset',  True],
    'use':    [f'{default_command_header}.use',    True]
}

for alias in aliases:
    try:
        aliases[alias][1] = False
    except IndexError:
        aliases[alias].append(False)
    

for default_token in default_command_dict:
    aliases[default_token] = default_command_dict[default_token]

temp_aliases = aliases.copy()
for alias_token in temp_aliases:
    is_alias = True
    command = aliases[alias_token][0]
    is_default: bool = aliases[alias_token][1]
    while is_alias:
        token = command.split()[0]
        # print('------------------------')
        # print(alias_token, '->', aliases.get(alias_token))
        if aliases.get(token):
            if aliases.get(token)[0].split()[0] == token:
                is_alias = False
            else:
                command = command.replace(token, aliases.get(token, [token])[0], 1)
        else:
            is_alias = False
    # print(alias_token, '->', command)
    aliases[alias_token] = [command, is_default]

#List valid modules from config.json
valid_modules: dict = data['modules']

#Read the rules for valid options
option_dict: dict = data['options']

#Override options with values provided by the user
for option in option_dict:
    if OPTIONS.get(option):
        if option_dict[option]['type'] == "dict": option_dict[option]['value']['value'] = OPTIONS.get(option)
        else: option_dict[option]['value'] = OPTIONS.get(option)