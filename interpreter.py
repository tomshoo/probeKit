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

import modules.util.utils as utils

print(f'Importing custom modules', end='\r')
start = utils.timestamp()
import modules.data.AboutList as aboutList
import modules.util.exec as exec
from modules.data.OptInfHelp import PromptHelp, Options, Info
from config import colors, variables, aliases
from modules.util.led import start_editor
end = utils.timestamp()
print(f'modules took {round(end-start, 7)} sec(s). to load')

# Setup Utils
args = utils.args
ExitException = utils.ExitException
datevalue = utils.datevalue
register_history = utils.register_history
completion_list: list = [
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
]
completer = utils.completer(completion_list)


# Setting up colors (edit these in config.py)
FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL
FURGENT = colors.FURGENT
FSTYLE = colors.FPROMPT

# Display time during statup
print(f'current session started at {datevalue()}')
utils.banner()

# Checks if history file already exists or not
if 'Linux' in platform.platform():
    histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')
    if os.path.exists(histfile):
        readline.read_history_file(histfile)

if 'Windows' in platform.platform():
    print(f'{FURGENT}[**] Warning: system commands will not run in windows based system')

# Session starts over here
# Not the best way to do it but it works so...
if 'Windows' not in platform.platform():
    if os.getuid() != 0:
        print(f'{FURGENT}[**] Warning: You won\'t be able to use the osprbe module without root access.')

def main(exitStatus: int = 0):
    check = 1 if args(sys.argv, 1) else 0
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
    # Initial module is set to blank
    # Set it to any other module if you want a default module at startup
    MODULE = variables.MODULE
    if MODULE in aboutList.moduleHelp.modules or MODULE == '':
        pass
    else:
        print(f'{FALERT}[-] No such module: \'{MODULE}\'{FNORMAL}')
        sys.exit(1)

    try:
        while (True):
            readline.set_completer(completer.completion)
            readline.parse_and_bind("tab: complete")

            if exitStatus == 0:
                COLOR = colors.FSUCCESS
            elif exitStatus == 3:
                COLOR = colors.FURGENT
            else:
                COLOR = colors.FALERT

            # Checks if module is activated or not
            if check == 0:
                if MODULE == '':
                    inputval = input(f'{FNORMAL}[probkit]: {COLOR}{exitStatus}{FNORMAL}$> ')
                else:
                    inputval = input(f'{FNORMAL}probeKit: {FSTYLE}[{MODULE}]: {COLOR}{exitStatus}{FSUCCESS}$>{FNORMAL} ')
            else:
                inputval = ' '.join(sys.argv[1].split('\ '))
                check = 0

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
                    inputval = utils.trim(inputlist.pop(0))
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
                    cmdSplit: list = []
                    cmdSplit_quote_delimeter: list = []

                    commands = utils.trim(commands)

                    aliasedcommand : list = commands.split()
                    calledAlias = args(aliasedcommand, 0)
                    aliasedcommand[0] = aliases.get(str(calledAlias), str(calledAlias))
                    commands = ' '.join(aliasedcommand)

                    # split the input to obtain command arguments
                    if commands  not in ['', None]:
                        cmdSplit_quote_delimeter = []
                        for l in csv.reader([commands], delimiter=' ', quotechar='"'):
                            cmdSplit_quote_delimeter = l
                        cmdSplit = commands.split()
                        verb = args(cmdSplit, 0)

                    # Check if given input is blank
                    # Helps in maintaining comments
                    # Need to find a better less messy way to handle comments
                    if commands in ['', None]:
                        exitStatus = 0

                    # Henceforth starts the if... elif... else for command based output
                    elif verb == "banner":
                        utils.banner()
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
                            exitStatus = 0
                        else:
                            print(chr(27)+'2[j')
                            print('\033c')
                            print('\x1bc')
                            exitStatus = 0

                        if args(cmdSplit, 1) == '-e':
                            sys.exit(exitStatus)

                    elif verb == 'run':
                        try:
                            exitStatus = exec.run(MODULE, OPTIONS)
                        except Exception as e:
                            print(e)

                    # Verb(or command) to set options
                    elif verb == 'set':
                        OPTIONS = exec.set(OPTIONS, args(cmdSplit, 1), args(cmdSplit, 2))
                        if args(OPTIONS, 8):
                            exitStatus = OPTIONS[8]
                            OPTIONS.pop(8)
                    # Verb(or command) to unset options
                    elif verb == 'unset':
                        OPTIONS = exec.unset(OPTIONS, args(cmdSplit, 1))
                        if args(OPTIONS, 8):
                            exitStatus = OPTIONS[8]
                            OPTIONS.pop(8)
                    
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
                                exitStatus = subprocess.run(commands, shell=True).returncode
                        
                        except FileNotFoundError:
                            print(f'{FALERT}Error: Invalid command \'{verb}\'')
                            exitStatus = 1
                        
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
                sys.exit(exitStatus)

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
        print(f'\n')
        main(exitStatus=3)
        pass

if __name__ == '__main__':
    main()
