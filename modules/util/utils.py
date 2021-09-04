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