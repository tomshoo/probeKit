#! /usr/bin/env python3
"""
Interpreter for the entire probeKit
"""

# Imports
import sys
import readline
import os
from modules.data.OptInfHelp import PromptHelp, Options, Info
import modules.data.AboutList as aboutList
from config import colors, variables, aliases
from modules.run import run

# Setting up colors (edit these in config.py)
FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL
FURGENT = colors.FURGENT
FSTYLE = colors.FPROMPT

# Custom exception to exit the session
class ExitException(Exception):
    pass

# Function to remove extra white spaces from the string
def trim(string):
    strsplit : list = string.split()
    return ' '.join(strsplit)

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

# Function to get immediate time at a point
def datevalue():
    from datetime import datetime
    return datetime.now().strftime('%a %F %H:%M:%S')

print(f'current session started at {datevalue()}')
banner()

# Initial module is set to blank
# Set it to any other module if you want a default module at startup
MODULE = ''

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

# Checks if history file already exists or not 
histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')
if os.path.exists(histfile):
  readline.read_history_file(histfile)

# Just a simple function to return values in a list and raise exception
# in such a way that the prog. doesn't break
def __returnval(value, pos):
    try:
        return str(value[int(pos)])
    except Exception:
        return ''

# Variables also known as options to the user
OPTIONS = [variables.LHOST
 , variables.LPORT
 , variables.PROTOCOL
 , variables.TIMEOUT
 , variables.TRYCT
 , variables.NMAP
 , variables.VERBOSE
]
exitStatus = 0

# Session starts over here
# Not the best way to do it but it works so...
try:
    while (True):

        if exitStatus == 0:
            COLOR = colors.FSUCCESS
        elif exitStatus == 'idle':
            COLOR = colors.FURGENT
        else:
            COLOR = colors.FALERT

        # Checks if module is activated or not
        if MODULE == '':
            inputval = input(f'{FNORMAL}[probkit]: {COLOR}{exitStatus}{FNORMAL}$> ')
        else:
            inputval = input(FNORMAL+'probeKit:'+FSTYLE+f'[{MODULE}]'+FSUCCESS+' $> '+FNORMAL)

        # Call the register_history class to write history
        # Adds time stamp to each command after the session has ended
        register_history(inputval).write_history()

        # Split the command using a ';' helps in scripting support (or)
        # multiple commands in a single line
        try:
            if inputval[len(inputval)-1::] != ';':
                valsplit = list(inputval)
                valsplit.append(';')
                inputval = ''.join(valsplit)

            commadlist : list = inputval.split(';')
            commadlist.pop(len(commadlist)-1)

            # Interate everything for commands stored in the commanlist
            for commands in commadlist:
                verb = ''
                cmdSplit = []

                commands = trim(commands)

                aliasedcommand : list = commands.split()
                calledAlias = __returnval(aliasedcommand, 0)
                aliasedcommand[0] = aliases.get(str(calledAlias), str(calledAlias))
                commands = ' '.join(aliasedcommand)

                # Check if the given input was a comment
                # Will not work if the input has a ';'
                # Need to create an escape character for that
                # something like '\;'
                if commands[0] == '#':
                    commands = ''
                elif '#' in commands:
                    commands = commands[:commands.index('#'):]

                # split the input to obtain command arguments
                if commands  not in ['', None]:
                    cmdSplit = commands.split()
                    verb = __returnval(cmdSplit, 0)

                # Check if given input is blank
                # Helps in maintaining comments
                # Need to find a better less messy way to handle comments
                if commands in ['', None]:
                    exitStatus = 0

                # Henceforth starts the if... elif... else for command based output
                elif verb == "banner":
                    banner()

                elif verb == 'help':
                  if not __returnval(cmdSplit, 1):
                    Data = PromptHelp('')
                    Data.showHelp()
                  else:
                    Data = PromptHelp(__returnval(cmdSplit, 1))
                    Data.showHelp()

                elif verb == 'list':
                    aboutList.moduleHelp(MODULE).listmodules()

                elif verb == 'show':
                    if __returnval(cmdSplit, 1):
                        if __returnval(cmdSplit, 1) == 'info':
                            info = Info(MODULE, OPTIONS)
                            try:
                                info.showInfo()
                            except Exception as e:
                                print(e)

                            exitStatus = 0

                        elif __returnval(cmdSplit, 1) == 'options':
                            Option = Options(MODULE)
                            try:
                                Option.showOptions()
                            except Exception as e:
                                print(e)

                        elif __returnval(cmdSplit, 1) == 'status':
                            print(exitStatus)
                            exitStatus = 0

                        else:
                            print(f'{FALERT}[-] Error: Invalid argument provided')
                            exitStatus = 1
                    else:
                        print(f'{FALERT}[-] Error: no argument provided')
                        exitStatus = 1

                elif verb == 'back':
                    if MODULE == '':
                        raise ExitException(f'{FALERT}probeKit: exiting session')
                    else:
                        MODULE = ''

                # Create an exception which exits the try block and then exits the session
                elif verb == 'exit':
                    raise ExitException(f'{FALERT}probeKit: exiting session')

                elif verb == 'clear':
                    print(chr(27)+'2[j')
                    print('\033c')
                    print('\x1bc')
                    exitStatus = 0

                elif verb == 'run':
                    try:
                        run(MODULE, OPTIONS)
                    except Exception as e:
                        print(e)

                # Verb(or command) to set options
                elif verb == 'set':
                    # if the first argument is 'all' all values default to those specified in config.py
                    if __returnval(cmdSplit, 2) and __returnval(cmdSplit, 1) != 'all':
                        if __returnval(cmdSplit, 1) in ['LHOST', 'lhost']:
                            print(f'LHOST => {__returnval(cmdSplit, 2)}')
                            OPTIONS[0] = __returnval(cmdSplit, 2)

                        elif __returnval(cmdSplit, 1) in ['LPORT', 'lport']:
                            if '/' in __returnval(cmdSplit, 2):
                                OPTIONS[1] = __returnval(cmdSplit, 2).split('/')
                                print(f'LPORT => {OPTIONS[1]}')

                            else:
                                print(f'LPORT => {__returnval(cmdSplit, 2)}')
                                OPTIONS[1] = __returnval(cmdSplit, 2)

                        elif __returnval(cmdSplit, 1) in ['PROTO', 'proto']:
                            print(f'PROTO => {__returnval(cmdSplit, 2)}')
                            OPTIONS[2] = __returnval(cmdSplit, 2)

                        elif __returnval(cmdSplit ,1) in ['TMOUT', 'tmout']:
                            print(f'TMOUT => {__returnval(cmdSplit, 2)}')
                            OPTIONS[3] = __returnval(cmdSplit, 2)

                        elif __returnval(cmdSplit, 1) in ['TRYCT', 'tryct']:
                            print(f'TRYCT => {__returnval(cmdSplit, 2)}')
                            OPTIONS[4] = int(__returnval(cmdSplit, 2))

                        elif __returnval(cmdSplit, 1) in ['NMAP', 'nmap']:
                            print(f'NMAP  => {__returnval(cmdSplit, 2)}')
                            OPTIONS[5] = int(__returnval(cmdSplit, 2))

                        elif __returnval(cmdSplit, 1) in ['VERBOSE', 'verbose']:
                            if __returnval(cmdSplit, 2) not in ['true', 'false']:
                                print(FALERT+'Error: Invalid value provided')
                            elif __returnval(cmdSplit, 2) == 'true':
                                OPTIONS[6] = True
                                print(f'VERBOSE => {OPTIONS[6]}')
                            elif __returnval(cmdSplit, 2) == 'false':
                                OPTIONS[6] = False
                                print(f'VERBOSE => {OPTIONS[6]}')

                        else:
                            print(FALERT+'[-] Error: Invalid option')

                    # If there are no values in the config.py then,
                    # this is same as `unset all`
                    elif __returnval(cmdSplit, 1) == 'all':
                        OPTIONS[0] = variables.LHOST
                        OPTIONS[1] = variables.LPORT
                        OPTIONS[2] = variables.PROTOCOL
                        OPTIONS[3] = variables.TIMEOUT
                        OPTIONS[4] = variables.TRYCT
                        OPTIONS[5] = variables.NMAP
                        OPTIONS[6] = variables.VERBOSE

                    elif not __returnval(cmdSplit, 2):
                        print(f'{FALERT}[-] Error: no value provided to option')

                    else:
                        print(f"{FALERT}[-] Error: Invalid value provided to option")

                # Verb(or command) to unset options
                elif verb == 'unset':
                    if __returnval(cmdSplit, 1) in ['LHOST', 'lhost']:
                        print(f'{FALERT}unset LHOST')
                        OPTIONS[0] = ''

                    elif __returnval(cmdSplit, 1) in ['LPORT', 'lport']:
                        print(f'{FALERT}unset LPORT')
                        OPTIONS[1] = ''

                    elif __returnval(cmdSplit, 1) in ['PROTO', 'proto']:
                        print(f'{FALERT}unset PROTO')
                        OPTIONS[2] = ''

                    elif __returnval(cmdSplit, 1) in ['TMOUT', 'tmout']:
                        print(f'{FALERT}unset TMOUT')
                        OPTIONS[3] = '1'

                    elif __returnval(cmdSplit, 1) in ['TRYCT', 'tryct']:
                        print(f'{FALERT}unset TRYCT')
                        OPTIONS[4] = 1

                    elif __returnval(cmdSplit, 1) in ['NMAP', 'nmap']:
                        print(f'{FALERT}unset NMAP')
                        OPTIONS[5] = 0

                    elif __returnval(cmdSplit, 2) in ['VERBOSE', 'verbose']:
                        print(f'{FALERT}unset VERBOSE')
                        OPTIONS[6] = ''

                    elif __returnval(cmdSplit, 1) == 'all':
                        OPTIONS[0] = ''
                        OPTIONS[1] = ''
                        OPTIONS[2] = ''
                        OPTIONS[3] = 1
                        OPTIONS[4] = 1
                        OPTIONS[5] = 0
                        OPTIONS[6] = ''
                    else:
                        print(FALERT+'Error: Invalid option')

                elif verb == 'use':
                    if __returnval(cmdSplit, 1):
                        if __returnval(cmdSplit, 1) in aboutList.moduleHelp.modules:
                            MODULE = __returnval(cmdSplit, 1)
                            print(FURGENT+f'MODULE => {MODULE}')
                        else:
                            print(f'{FALERT}Error: Invalid module specified: \'{__returnval(cmdSplit, 1)}\'')
                    else:
                        print(FALERT+'Error: No module specified')

                elif verb == 'about':
                    if __returnval(cmdSplit, 1):
                        mod = __returnval(cmdSplit, 1)
                        aboutList.moduleHelp(mod).aboutModule(mod)
                    else:
                        aboutList.moduleHelp(MODULE).aboutModule(MODULE)

                elif verb == 'alias':
                    try:
                        if not __returnval(cmdSplit, 1):
                            for x in aliases:
                                print(x,":",aliases[x])

                        else:
                            splitCommand = commands.split('=')
                            assignedCommand = splitCommand[1]
                            alias = splitCommand[0].split()[1]
                            if not assignedCommand or assignedCommand == '':
                                print(f'{FALERT}[-] Error: please provide a command to alias')
                            else:
                                print(alias, "=>",assignedCommand)
                                aliases[alias]=assignedCommand

                    except Exception as e:
                        print(e)
                        pass

                elif verb == 'unalias':
                    if __returnval(cmdSplit, 1) and __returnval(cmdSplit, 1) in aliases:
                        del aliases[__returnval(cmdSplit, 1)]
                    else:
                        print(f'{FALERT}[-] Error: no such alias \'{FURGENT}{__returnval(cmdSplit, 1)}{FALERT}\' exists')

                else:
                    print(f'{FALERT}[-] Error: Invalid command \'{verb}\'{FNORMAL}')

        # Write the date and time when the session was ended to the history
        # Helps in finding those specific commands we try to remember
        except ExitException as e:
            with open(histfile, 'a') as fp:
              fp.write('# session ended at: ' + datevalue() + ' # \n')
              pass
            print(e)
            sys.exit(0)

        # Except the index error in the main try block and pass an idle exit status
        # Helps in keeping the session active even if no input was given before enter
        except IndexError:
            exitStatus = 'idle'
            pass

# Does the same as ExitException nothing new
except EOFError as E:
    with open(histfile, 'a') as fp:
        fp.write('# session ended at: ' + datevalue() + ' # \n')
        pass

    print(f'\n{FALERT}probeKit: exiting session')
    sys.exit()

except Exception as e:
    print(e)
