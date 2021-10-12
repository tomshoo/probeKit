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