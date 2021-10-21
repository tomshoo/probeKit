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
    def completion(self, text, state):
        """return valid commands from the list of commands provided"""
        commands = self.commands
        options = [i for i in commands if i.startswith(text)]
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

    return datetime.now().strftime('%a %F %H:%M:%S')

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

    def write_history(self):
        """write the history to $HOME/.probeKit.history"""
        histfile = self.histfile
        if os.path.exists(histfile):
            with open(histfile, 'a') as fp:
                fp.write(self.command + f' # {datevalue()} \n')
                pass
        else:
            with open(histfile, 'w') as fp:
                fp.write(self.command + f' # {datevalue()} \n')
                pass

@dispatch(dict)
def optionparser(option_dict: dict) -> dict:
    for data in option_dict:
        if args(option_dict[data]['type'].split(), 0) == "dict":
            _type = option_dict[data]['type'].split()
            value_rules = _type[1::]
            for rule in value_rules:
                rule = rule.split('_')
                value_type = args(rule, 0)
                value_dtype = args(rule, 1).split('-') if '-' in args(rule, 1) else args(rule, 1)
                _dtype_primary = value_dtype[0]
                _dtype_secondary = value_dtype[1]
                if _dtype_primary == 'list':
                    value_delm = args(rule, 2)
                    if value_delm in option_dict[data]['value']['value']:
                        option_dict[data]['value']['type'] = value_type
                        option_dict[data]['value']['value'] = option_dict[data]['value']['value'].split(value_delm)
                else:
                    option_dict[data]['value']['type'] = value_type

        else:
            if option_dict[data]['value']:
                if option_dict[data]['type'] == "int": 
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