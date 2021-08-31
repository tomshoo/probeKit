"""
* This file contains all the necessary utilities required for other
programs or modules.

* If you want to create some other utility please create it in this
file and later import it from here.
"""

# Imports
from datetime import datetime
import time
import os

# Function to print the introductory banner
def banner():
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

# Just a simple function to return values in a list and raise exception
# in such a way that the prog. doesn't break
def args(value, pos):
    try:
        return str(value[int(pos)])
    except Exception:
        return ''

# Function to remove extra white spaces from the string
def trim(string):
    strsplit : list = string.split()
    return ' '.join(strsplit)

# Custom exception to exit the session
class ExitException(Exception):
    pass

# Function to get immediate time at a point
def datevalue():
    return datetime.now().strftime('%a %F %H:%M:%S')

# To get total time taken by things to load and run
def timestamp():
    return time.perf_counter()

# Class to register history
class register_history():
    def __init__(self, command : str):
        self.command = command
        self.histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')

    def write_history(self):
        histfile = self.histfile
        if os.path.exists(histfile):
            with open(histfile, 'a') as fp:
                fp.write(self.command + f' # {datevalue()} \n')
                pass
        else:
            with open(histfile, 'w') as fp:
                fp.write(self.command + f' # {datevalue()} \n')
                pass