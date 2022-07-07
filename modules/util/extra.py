"""
This file contains all the necessary utilities required for other
programs or modules.

If you want to create some other utility please create it in this
file and later import it from here.
"""

import ctypes
import os
import sys
import time
from collections import namedtuple

# Imports
from datetime import datetime
from typing import Any

from multipledispatch import dispatch
from rich import traceback

traceback.install()

# Named tuple containing all available commands for both `interpreter`, `probekit`
Completer = namedtuple("Completer", ["interpreter", "led"])
completers = Completer(
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
        "unset",
    ],
    [
        "i",
        "insert",
        "w",
        "write",
        "c",
        "change",
        "p",
        "print",
        "n",
        "lineprint",
        "q",
        "quit",
    ],
)


@dispatch(list, int)
def get_args(value: list[Any] | str, pos: int) -> str | None:
    """
    A simple function to return values in a list and raise exception
    in such a way that the interpreter doesn't break
    """
    if type(pos) is not int:
        raise TypeError(f"error at argument: pos, required `int` found {type(pos)}")
    if not (type(value) is list or type(value) is str):
        raise TypeError(f"error at argument: pos, required `list | str` found {type(str)}")

    try:
        return str(value[int(pos)])
    except Exception:
        return None

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


class string(str):
    def isfloat(self) -> bool:
        ssplit = self.split(".")
        length: int = len(ssplit)
        FloatList: list = []
        if 0 < length <= 2:
            for x in ssplit:
                FloatList.append(x.isdecimal())
            if False in FloatList:
                return False
            else:
                return True
        else:
            return False


def trim(string: str, delimiter: str = " ") -> str:
    """Function to remove extra white spaces from the string"""

    strsplit: list = string.split() if delimiter == " " else string.split(delimiter)
    breaker: int = 0
    for char in strsplit:
        if not char:
            breaker += 1
    counter: int = 0
    if delimiter != " ":
        while True:
            for idx, char in enumerate(strsplit):
                if not char:
                    strsplit.pop(idx)
            counter += 1
            if counter == breaker:
                break

    return delimiter.join(strsplit)


class ExitException(Exception):
    """Custom "dummy" exception to exit the session"""

    pass


def ExitSession(exitStatus: int, histfile: str | None = None):
    if histfile is None:
        sys.exit(exitStatus)
    else:
        with open(histfile, "a") as fp:
            fp.write("# session ended at: " + timefunc.datevalue() + " # \n")
            pass
        sys.exit(exitStatus)


def isAdmin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        return os.getuid() == 0


class timefunc:
    @staticmethod
    def datevalue() -> str:
        """Function to get immediate time at a point"""

        return datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")

    @staticmethod
    def timestamp() -> float:
        """To get total time taken by things to load and run"""

        return time.perf_counter()
