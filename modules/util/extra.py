"""
This file contains all the necessary utilities required for other
programs or modules.

If you want to create some other utility please create it in this
file and later import it from here.
"""

# Imports
from datetime import datetime
import time
import ctypes
import sys
import os
from multipledispatch import dispatch
from rich import traceback
from collections import namedtuple
traceback.install()

# Named tuple containing all available commands for both `interpreter`, `probekit`
completer = namedtuple("Completers", ['interpreter', 'led'])
completers = completer(
    [
        "use", 
        "show", 
        "set", 
        "help", 
        "exit", 
        "back", 
        "clear", 
        "run", 
        "about", 
        "list", 
        "banner", 
        "alias", 
        "unalias", 
        "unset"
    ],
    [
        "i", "insert",
        "w", "write",
        "c", "change",
        "p", "print",
        "n", "lineprint",
        "q", "quit",
    ]
)

def args(value: list, pos: int) -> str:
    """
    A simple function to return values in a list and raise exception
    in such a way that the interpreter doesn't break
    """

    try: return str(value[int(pos)])
    except Exception: return ''

class completer:
    """tab completion class(experimental)"""
    def __init__(self, commands): self.commands = commands
    def completion(self, text: str, state: int):
        """return valid commands from the list of commands provided"""
        commands = self.commands
        options = [i for i in commands if i.startswith(text.lower())]
        if state < len(options): return options[state]
        else: return None

class string(str):
    def isfloat(self)->bool:
        ssplit = self.split('.')
        length: int = len(ssplit)
        FloatList: list = []
        if 0 < length <= 2:
            for x in ssplit:
                FloatList.append(x.isdecimal())
            if False in FloatList: return False
            else: return True
        else: return False

def trim(string: str, delimiter: str = " ") -> str:
    """Function to remove extra white spaces from the string"""

    strsplit : list = string.split() if delimiter == " " else string.split(delimiter)
    breaker: int = 0
    for char in strsplit:
        if not char: breaker+=1
    counter: int = 0
    if delimiter != " ":
        while True:
            for idx, char in enumerate(strsplit):
                if not char:
                    strsplit.pop(idx)
            counter+=1
            if counter == breaker: break
            
    return delimiter.join(strsplit)

class ExitException(Exception):
    """Custom "dummy" exception to exit the session"""
    pass

@dispatch(int)
def Exit(exitStatus: int): sys.exit(exitStatus)

@dispatch(int, str)
def Exit(exitStatus: int, histfile: str):
    """End the session and append the date and time to the end of the history file."""

    with open(histfile, 'a') as fp:
        fp.write('# session ended at: ' + timefunc.datevalue() + ' # \n')
        pass
    sys.exit(exitStatus)

def isAdmin() -> bool:
    try: return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError: return os.getuid() == 0

class timefunc:
    @staticmethod
    def datevalue() -> str:
        """Function to get immediate time at a point"""

        return datetime.now().strftime('%a %Y-%m-%d %H:%M:%S')

    @staticmethod
    def timestamp() -> float:
        """To get total time taken by things to load and run"""

        return time.perf_counter()