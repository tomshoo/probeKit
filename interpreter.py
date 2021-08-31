#! /usr/bin/env python3
"""
Interpreter for the entire probeKit
"""

# Imports
import sys
import readline
import platform
import csv
import os
import subprocess

import modules.utils as utils

print(f'Importing custom modules', end='\r')
start = utils.timestamp()
import modules.data.AboutList as aboutList
from modules.data.OptInfHelp import PromptHelp, Options, Info
from config import colors, variables, aliases
from modules.led import start_editor
end = utils.timestamp()
print(f'modules took {round(end-start, 7)} sec(s). to load')

# Setup Utils
banner = utils.banner
args = utils.args
trim = utils.trim
ExitException = utils.ExitException
datevalue = utils.datevalue
register_history = utils.register_history
run = utils.run

# Setting up colors (edit these in config.py)
FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL
FURGENT = colors.FURGENT
FSTYLE = colors.FPROMPT

# Display time during statup
print(f'current session started at {datevalue()}')
banner()

# Checks if history file already exists or not
if 'Linux' in platform.platform():
    histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')
    if os.path.exists(histfile):
        readline.read_history_file(histfile)

if 'Windows' in platform.platform():
    print(f'{FURGENT}[**] Warning: system commands will not run in windows based system')
# Variables also known as options to the user
OPTIONS : list = [
    variables.THOST
    , variables().tport()
    , variables().PROTOCOL
    , variables().timeout()
    , variables().trycount()
    , variables().Nmap()
    , variables().Verbose()
    , variables().Threading()
   ]

# Session starts over here
# Not the best way to do it but it works so...

if 'Windows' not in platform.platform():
    if os.getuid() != 0:
        print(f'{FURGENT}[**] Warning: You won\'t be able to use the osprbe module without root access.')

def main():
    # Initial module is set to blank
    # Set it to any other module if you want a default module at startup
    MODULE = variables.MODULE
    if MODULE in aboutList.moduleHelp.modules or MODULE == '':
        pass
    else:
        print(f'{FALERT}[-] No such module: \'{MODULE}\'{FNORMAL}')
        sys.exit(1)

    exitStatus = 0
    try:
        while (True):

            if exitStatus == 0:
                COLOR = colors.FSUCCESS
            elif exitStatus == 3:
                COLOR = colors.FURGENT
            else:
                COLOR = colors.FALERT

            # Checks if module is activated or not
            if MODULE == '':
                inputval = input(f'{FNORMAL}[probkit]: {COLOR}{exitStatus}{FNORMAL}$> ')
            else:
                inputval = input(f'{FNORMAL}probeKit: {FSTYLE}[{MODULE}]: {COLOR}{exitStatus}{FSUCCESS}$>{FNORMAL} ')

            # Call the register_history class to write history
            # Adds time stamp to each command after the session has ended
            register_history(inputval).write_history()

            # Split the command using a ';' helps in scripting support (or)
            # multiple commands in a single line
            # does not work if ';' is after a '#' tho
            try:
                # Check if the given input was a comment
                if '#' in inputval:
                    inputlist = inputval.split('#')
                    inputval = trim(inputlist.pop(0))
                else:
                    pass

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
                    calledAlias = args(aliasedcommand, 0)
                    aliasedcommand[0] = aliases.get(str(calledAlias), str(calledAlias))
                    commands = ' '.join(aliasedcommand)

                    # split the input to obtain command arguments
                    if commands  not in ['', None]:
                        cmdSplit: list = []
                        for l in csv.reader([commands], delimiter=' ', quotechar='"'):
                            cmdSplit = l
                        verb = args(cmdSplit, 0)

                    # Check if given input is blank
                    # Helps in maintaining comments
                    # Need to find a better less messy way to handle comments
                    if commands in ['', None]:
                        exitStatus = 0

                    # Henceforth starts the if... elif... else for command based output
                    elif verb == "banner":
                        banner()
                        exitStatus = 0

                    elif verb == 'help':
                      if not args(cmdSplit, 1):
                        Data = PromptHelp('')
                        exitStatus = Data.showHelp()
                      else:
                        Data = PromptHelp(args(cmdSplit, 1))
                        exitStatus = Data.showHelp()

                    elif verb == 'led':
                        init_editor = start_editor(cmdSplit)
                        init_editor.start_led()

                    elif verb == 'list':
                        exitStatus = aboutList.moduleHelp(MODULE).listmodules()

                    elif verb == 'show':
                        if args(cmdSplit, 1):
                            if args(cmdSplit, 1) == 'options':
                                options = Options(MODULE, OPTIONS)
                                options.showOptions()
                                exitStatus = 0

                            elif args(cmdSplit, 1) == 'info':
                                info = Info(MODULE)
                                exitStatus = info.showInfo()

                            elif args(cmdSplit, 1) == 'status':
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
                            exitStatus = 0

                    # Create an exception which exits the try block and then exits the session
                    elif verb == 'exit':
                        raise ExitException(f'{FALERT}probeKit: exiting session{FNORMAL}')

                    elif verb == 'clear':
                        if 'Windows' in platform.platform():
                            os.system('cls')
                        else:
                            print(chr(27)+'2[j')
                            print('\033c')
                            print('\x1bc')
                            exitStatus = 0

                    elif verb == 'run':
                        try:
                            exitStatus = run(MODULE, OPTIONS)
                        except Exception as e:
                            print(e)

                    # Verb(or command) to set options
                    elif verb == 'set':
                        # if the first argument is 'all' all values default to those specified in config.py
                        if args(cmdSplit, 2) and args(cmdSplit, 1) != 'all':
                            if args(cmdSplit, 1) in ['THOST', 'thost']:
                                print(f'THOST => {args(cmdSplit, 2)}')
                                OPTIONS[0] = args(cmdSplit, 2)

                            elif args(cmdSplit, 1) in ['TPORT', 'tport']:
                                if '/' in args(cmdSplit, 2):
                                    OPTIONS[1] = args(cmdSplit, 2).split('/')
                                    print(f'TPORT => {OPTIONS[1]}')

                                else:
                                    print(f'TPORT => {args(cmdSplit, 2)}')
                                    OPTIONS[1] = args(cmdSplit, 2)

                            elif args(cmdSplit, 1) in ['PROTO', 'proto', 'protocol', "PROTOCOL"]:
                                print(f'PROTO => {args(cmdSplit, 2)}')
                                OPTIONS[2] = args(cmdSplit, 2)

                            elif args(cmdSplit ,1) in ['TMOUT', 'tmout']:
                                print(f'TMOUT => {args(cmdSplit, 2)}')
                                OPTIONS[3] = args(cmdSplit, 2)

                            elif args(cmdSplit, 1) in ['TRYCT', 'tryct']:
                                print(f'TRYCT => {args(cmdSplit, 2)}')
                                OPTIONS[4] = int(args(cmdSplit, 2))

                            elif args(cmdSplit, 1) in ['NMAP', 'nmap']:
                                print(f'NMAP  => {args(cmdSplit, 2)}')
                                OPTIONS[5] = int(args(cmdSplit, 2))

                            elif args(cmdSplit, 1) in ['VERBOSE', 'verbose']:
                                if args(cmdSplit, 2) not in ['true', 'false']:
                                    print(FALERT+'Error: Invalid value provided')
                                elif args(cmdSplit, 2) == 'true':
                                    OPTIONS[6] = True
                                    print(f'VERBOSE => {OPTIONS[6]}')
                                elif args(cmdSplit, 2) == 'false':
                                    OPTIONS[6] = False
                                    print(f'VERBOSE => {OPTIONS[6]}')

                            elif args(cmdSplit, 1) in ['THREADING', 'threading']:
                                if args(cmdSplit, 2) not in ['true', 'True', 'false', 'False']:
                                    print(f'{FALERT}Error: Invalid value provided')
                                elif args(cmdSplit, 2) in ['true', 'True']:
                                    OPTIONS[7] = True
                                else:
                                    OPTIONS[7] = False
                                print(f'THREADING => {OPTIONS[7]}')

                            else:
                                print(FALERT+'[-] Error: Invalid option')

                        # If there are no values in the config.py then,
                        # this is same as `unset all`
                        elif args(cmdSplit, 1) == 'all':
                            OPTIONS[0] = variables.THOST
                            OPTIONS[1] = variables.tport()
                            OPTIONS[2] = variables.PROTOCOL
                            OPTIONS[3] = variables.timeout()
                            OPTIONS[4] = variables.trycount()
                            OPTIONS[5] = variables.Nmap()
                            OPTIONS[6] = variables.Verbose()
                            OPTIONS[7] = variables.Threading()

                        elif not args(cmdSplit, 2):
                            print(f'{FALERT}[-] Error: no value provided to option')

                        else:
                            print(f"{FALERT}[-] Error: Invalid value provided to option")

                    # Verb(or command) to unset options
                    elif verb == 'unset':
                        if args(cmdSplit, 1) in ['THOST', 'thost']:
                            print(f'{FALERT}unset THOST')
                            OPTIONS[0] = ''

                        elif args(cmdSplit, 1) in ['TPORT', 'tport']:
                            print(f'{FALERT}unset TPORT')
                            OPTIONS[1] = ''

                        elif args(cmdSplit, 1) in ['PROTO', 'proto', 'protocol', 'PROTOCOL']:
                            print(f'{FALERT}unset PROTO')
                            OPTIONS[2] = ''

                        elif args(cmdSplit, 1) in ['TMOUT', 'tmout']:
                            print(f'{FALERT}unset TMOUT')
                            OPTIONS[3] = 1

                        elif args(cmdSplit, 1) in ['TRYCT', 'tryct']:
                            print(f'{FALERT}unset TRYCT')
                            OPTIONS[4] = 1

                        elif args(cmdSplit, 1) in ['NMAP', 'nmap']:
                            print(f'{FALERT}unset NMAP')
                            OPTIONS[5] = 0

                        elif args(cmdSplit, 1) in ['VERBOSE', 'verbose']:
                            print(f'{FALERT}unset VERBOSE')
                            OPTIONS[6] = ''

                        elif args(cmdSplit, 1) in ['THREADING', 'threading']:
                            print(f'{FALERT}unset THREADING')
                            OPTIONS[7] = ''

                        elif args(cmdSplit, 1) == 'all':
                            OPTIONS[0] = ''
                            OPTIONS[1] = ''
                            OPTIONS[2] = ''
                            OPTIONS[3] = 1
                            OPTIONS[4] = 1
                            OPTIONS[5] = 0
                            OPTIONS[6] = ''
                            OPTIONS[7] = ''
                        else:
                            print(FALERT+'Error: Invalid option')

                    elif verb == 'use':
                        if args(cmdSplit, 1):
                            if args(cmdSplit, 1) in aboutList.moduleHelp.modules:
                                MODULE = args(cmdSplit, 1)
                                print(FURGENT+f'MODULE => {MODULE}')
                                exitStatus = 0
                            else:
                                print(f'{FALERT}Error: Invalid module specified: \'{args(cmdSplit, 1)}\'')
                                exitStatus = 1
                        else:
                            print(FALERT+'Error: No module specified')
                            exitStatus = 1

                    elif verb == 'about':
                        if args(cmdSplit, 1):
                            mod = args(cmdSplit, 1)
                            aboutList.moduleHelp(mod).aboutModule(mod)
                        else:
                            aboutList.moduleHelp(MODULE).aboutModule(MODULE)

                    elif verb == 'alias':
                        if not args(cmdSplit, 1):
                            exitStatus = 0
                            for x in aliases:
                                print(x,":",aliases[x])

                        elif args(cmdSplit, 1) and len(commands.split('=')) == 2:
                            splitCommand = commands.split('=')
                            assignedCommand = splitCommand[1]
                            alias = splitCommand[0].split()[1]
                            if not assignedCommand or assignedCommand == '':
                                print(f'{FALERT}[-] Error: please provide a command to alias')
                                exitStatus = 1
                            else:
                                print(alias, "=>",assignedCommand)
                                aliases[alias]=assignedCommand
                                exitStatus = 0

                        else:
                            print(f'{FALERT}[-] Error: Invalid Syntax')
                            exitStatus = 1

                    elif verb == 'unalias':
                        if args(cmdSplit, 1) and args(cmdSplit, 1) in aliases:
                            del aliases[args(cmdSplit, 1)]
                            exitStatus = 0
                        else:
                            print(f'{FALERT}[-] Error: no such alias \'{FURGENT}{args(cmdSplit, 1)}{FALERT}\' exists')
                            exitStatus = 1
                    elif verb in ['cd', 'chdir', 'set-location']:
                        fpath = args(cmdSplit, 1)
                        if os.path.exists(fpath) and os.path.isdir(fpath):
                            os.chdir(fpath)
                            print(f'dir: {fpath}')

                        else:
                            print(f'{FALERT}[-] Error: no such directory: \'{fpath}\'')

                    else:
                        try:
                            if 'Windows' not in platform.platform():
                                exitStatus = subprocess.call((cmdSplit))
                            else:
                                exitStatus = subprocess.run(commands, shell=True)
                        
                        except FileNotFoundError:
                            print(f'{FALERT}Error: Invalid command \'{verb}\'')
                        
                        except KeyboardInterrupt:
                            exitStatus = 130

            # Write the date and time when the session was ended to the history
            # Helps in finding those specific commands we try to remember
            except ExitException as e:
                if 'Linux' in platform.platform():
                    with open(histfile, 'a') as fp:
                        fp.write('# session ended at: ' + datevalue() + ' # \n')
                        pass
                print(e)
                sys.exit(0)

            # Except the index error in the main try block and pass an idle exit status
            # Helps in keeping the session active even if no input was given before enter
            except IndexError:
                exitStatus = 3
                pass

    # Does the same as ExitException nothing new
    except EOFError as E:
        if 'Linux' in platform.platform():
          with open(histfile, 'a') as fp:
            fp.write('# session ended at: ' + datevalue() + ' # \n')
            pass

        print(f'\n{FALERT}probeKit: exiting session{FNORMAL}')
        pass

    # Handles keyboard interupt by exiting and "not" wrinting `session ended at` to history
    except KeyboardInterrupt:
        print(f'\n{FALERT}probeKit: exiting session{FNORMAL}')
        pass

if __name__ == '__main__':
    main()
