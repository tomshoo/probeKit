"""
This file contains all the necessary utilities required for other
programs or modules.

If you want to create some other utility please create it in this
file and later import it from here.
"""

# Imports
from datetime import datetime
import time
import os
import ctypes
import sys
import csv
from multipledispatch import dispatch

def split_and_quote(key: str, quotekey: str, string: str) -> list:
    for l in csv.reader([string], delimiter=key, quotechar=quotekey):
        split_quoted = l
    return split_quoted

def args(value: list, pos: int) -> str:
    """
    A simple function to return values in a list and raise exception
    in such a way that the interpreter doesn't break
    """

    try:
        return str(value[int(pos)])
    except Exception:
        return ''

class completer:
    """tab completion class(experimental)"""
    def __init__(self, commands):
        self.commands = commands
    def completion(self, text: str, state: int):
        """return valid commands from the list of commands provided"""
        commands = self.commands
        options = [i for i in commands if i.startswith(text.lower())]
        if state < len(options):
            return options[state]
        else:
            return None


def isFloat(value: str) -> bool:
    """
    Check if a given string is a float value
    """
    valsplit = value.split('.')
    length: int = len(valsplit)
    isfloat: list = []
    if (0 < length <= 2):
        for x in valsplit:
            isfloat.append(x.isdecimal())
        if False in isfloat:
            return False
        else:
            return True
    else:
        return False

def trim(string: str) -> str:
    """Function to remove extra white spaces from the string"""

    strsplit : list = string.split()
    return ' '.join(strsplit)

class ExitException(Exception):
    """Custom "dummy" exception to exit the session"""
    pass

def datevalue() -> str:
    """Function to get immediate time at a point"""

    return datetime.now().strftime('%a %Y-%m-%d %H:%M:%S')

@dispatch(int)
def Exit(exitStatus: int):
    sys.exit(exitStatus)

@dispatch(int, str)
def Exit(exitStatus: int, histfile: str):
    """End the session and append the date and time to the end of the history file."""

    with open(histfile, 'a') as fp:
        fp.write('# session ended at: ' + datevalue() + ' # \n')
        pass
    sys.exit(exitStatus)

def isAdmin() -> bool:
    try:
        admin = ctypes.windll.shell32.IsUserAnAdmin() == 1
        return admin
    except AttributeError:
        return os.getuid() == 0

def timestamp() -> float:
    """To get total time taken by things to load and run"""

    return time.perf_counter()

class register_history():
    """
    Class to register history,

    * Does not work in windows. *
    """

    def __init__(self, command : str):
        self.command = command
        self.histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')

    def __hastimestamp(self) -> bool:
        command: str = self.command
        if '#' in command:
            comment_index: str = command.index('#')
            comment = command[comment_index+1::]
            comment = trim(comment)
            try:
                time.strptime(comment, "%a %Y-%m-%d %H:%M:%S")
                return True
            except ValueError:
                return False
        else:
            return False

    def write_history(self):
        """write the history to $HOME/.probeKit.history"""
        histfile = self.histfile
        if not self.__hastimestamp():
            if os.path.exists(histfile):
                with open(histfile, 'a') as fp:
                    fp.write(self.command + f' # {datevalue()} \n')
                    pass
            else:
                with open(histfile, 'w') as fp:
                    fp.write(self.command + f' # {datevalue()} \n')
                    pass


class optionsparser:
    def __init__(self, option_dict: dict) -> None:
        self.option_dict = option_dict

    def __dictparser(self, data: str) -> None:
        option_dict: dict = self.option_dict
        data_value: str  = option_dict[data]['value']
        data_rules: dict = option_dict[data]['typerules']
        if type(data_value['value']) is str:
            for scheme in data_rules:
                rule: dict = data_rules.get(scheme)
                identifier: str = rule.get('identifier')
                if identifier:
                    if identifier in data_value['value']: 
                        if rule.get('type') == "list":
                            data_value['type'] = scheme
                            if rule.get('delimeter'):
                                data_value['value'] = data_value['value'].split(rule.get('delimeter'))
                                break
                            else:
                                print('Err: no delimeter found... cannot split.')
                        else:
                            dtype = rule.get('dtype')
                            _type = rule.get('type')
                            exec(f'data_value[\'value\'] = {dtype}(\'{data_value["value"]}\')')
                            data_value['type'] = scheme
                            break
                else:
                    exec(f'''try:\n\tdata_value[\'value\'] = {rule.get("dtype")}(\'{data_value["value"]}\') if data_value[\'value\'] else \'\'\nexcept ValueError:\n\tprint(\'Err: Invalid value\')''')
                    data_value['type'] = scheme
        self.option_dict = option_dict

    def parse(self) -> dict:
        option_dict = self.option_dict
        for data in option_dict:
            if option_dict[data].get('value') is None:
                if option_dict[data].get('type') == "dict":
                    option_dict[data]['value'] = {
                        'value': '',
                        'type': ''
                    }
                else:
                    option_dict[data]['value'] = ''

            if option_dict[data].get('type'):
                if option_dict[data]['type'] == "dict":
                    if not option_dict[data].get('typerules'):
                        print('Err: No type rule found... skipping value')
                    else:
                        if type(option_dict[data]['typerules']) is not dict:
                            print('Invalid type rule scheme... skipping value')
                        else:
                            try:
                                self.__dictparser(data)
                            except TypeError as e:
                                print(f'Something went wrong... => {e}')
                    pass

                elif option_dict[data]['type'] == "int": 
                    if type(option_dict[data]['value']) is not int:
                        if option_dict[data]['value'].isdecimal():
                            option_dict[data]['value'] = int(option_dict[data]['value'])
                        else:
                            option_dict[data]['value'] = ""
                    else:
                        pass

                elif option_dict[data]['type'] == "float": 
                    if type(option_dict[data]['value']) is not float:
                        if isFloat(option_dict[data]['value']):
                            option_dict[data]['value'] = float(option_dict[data]['value'])
                        else:
                            option_dict[data]['value'] = ""
                    else:
                        pass

                elif option_dict[data]['type'] == "bool":
                    if type(option_dict[data]['value']) is not bool:
                        if option_dict[data]['value'].lower() in ['true', 'false']:
                            if option_dict[data]['value'].lower() == "true":
                                option_dict[data]['value'] = True
                            else:
                                option_dict[data]['value'] = False
                        else:
                            option_dict[data]['value'] = ""
                    else:
                        pass

                elif option_dict[data]['type'] == "str":
                    pass

                else:
                    _type = option_dict[data]['type']
                    print(f'Error: Invalid type: {_type}')
                    sys.exit(1)

        return option_dict