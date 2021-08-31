"""
* This file contains all the necessary utilities required for other
programs or modules.

* If you want to create some other utility please create it in this
file and later import it from here.
"""

# Imports
from datetime import datetime
from modules.data.AboutList import moduleHelp
import time
import os
from config import colors

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

# Function to provide the run command
def run(module, options):
    import modules.probe.ports as ports
    import modules.probe.osprobe as osprobe
    FALERT = colors.FALERT
    BALERT = colors.BALERT
    BNORMAL = colors.BNORMAL
    if module in moduleHelp(module).modules:
        try:
            lhost    = options[0]
            lport    = options[1]
            protocol = options[2]
            timeout  = options[3]
            tryct    = options[4]
            nmap     = options[5]
            verbose  = options[6]
            threading= options[7]
            try:
                if lhost == '':
                    print(FALERT+'Error: Invalid value for LHOST')
                else:
                    if module == 'probe':
                        if lport == '':
                            print(FALERT+'Error: value for LPORT')

                        ports.display(lhost, lport, timeout, protocol, tryct, verbose, threading)
                        return 0

                    elif module == 'osprobe':
                        osprobe.checkOS(lhost, tryct, nmap).scanner()
                        return 0

            except Exception as e:
                print(e)
                return 1

        except KeyboardInterrupt:
            print(FALERT+'\nalert: KeyboardInterrupt detected\n')
            return 2

    else:
        print(f'{BALERT}[-] Error: Invalid module \'{module}\'{BNORMAL}')
        return 1