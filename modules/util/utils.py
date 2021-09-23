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

def banner():
    """Function to print the introductory banner"""

    print('''
                          *               *    *          *
                          *               *   *     *     *
                          *               *  *            *
    * ***   * **   ****   * ***    ****   * *      **    ****
    **   *   *    *    *  **   *  *    *  **        *     *
    *    *   *    *    *  *    *  ******  * *       *     *
    **   *   *    *    *  *    *  *       *  *      *     *
    * ***    *    *    *  **   *  *    *  *   *     *     *  *
    *        *     ****   * ***    ****   *    *  *****    **
    *
    *

    -- by theEndurance-del
    ''')

def args(value, pos):
    """
    A simple function to return values in a list and raise exception
    in such a way that the interpreter doesn't break
    """

    try:
        return str(value[int(pos)])
    except Exception:
        return ''

#Setting up tab completion(experimental)
class completer:
    def __init__(self, commands):
        self.commands = commands
    def completion(self, text, state):
        commands = self.commands
        options = [i for i in commands if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None


def isFloat(value: str):
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

def trim(string):
    """Function to remove extra white spaces from the string"""

    strsplit : list = string.split()
    return ' '.join(strsplit)

class ExitException(Exception):
    """Custom "dummy" exception to exit the session"""
    pass

def datevalue():
    """Function to get immediate time at a point"""

    return datetime.now().strftime('%a %F %H:%M:%S')

def timestamp():
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