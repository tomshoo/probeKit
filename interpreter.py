#!/usr/bin/env python3

# Imports
import sys
import readline
import platform
import os
import ctypes
import subprocess

import modules.util.utils as utils

print(f'Importing custom modules', end='\r')
start = utils.timestamp()
import modules.data.AboutList as aboutList
from commands import (
    run,
    set as setval,
    unset,
    alias,
    unalias,
    use,
    banner
)
from modules.data.OptInfHelp import (PromptHelp, Options, Info)
from config import (
    MODULE,
    colors,
    aliases,
    option_dict,
    valid_modules as _modules
)
from modules.util.led import start_editor
end = utils.timestamp()
print(f'modules took {round(end-start, 7)} sec(s). to load')

# Setup Utils
optionparser = utils.optionsparser(option_dict)
option_dict = optionparser.parse()
ExitException = utils.ExitException
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
print(f'current session started at {utils.datevalue()}')
banner.run()

# Checks if history file already exists or not
if 'Windows' not in platform.platform():
    histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')
    if os.path.exists(histfile):
        readline.read_history_file(histfile)

    if os.getuid() != 0:
        print(f'{FURGENT}[**] Warning: You won\'t be able to use the osprbe module without root access.')

else:
    print(f'{FURGENT}[**] Warning: system commands will not run in windows based system')


# Session starts over here
# Not the best way to do it but it works so...

class input_parser:

    def __init__(self):
        self.exit_code: int = 0
        # Variables also known as options to the user
        self.option_dict = option_dict

        self.MODULE = MODULE
        self.aliases = aliases

    def parser(self, value: str):
        if '#' in value:
            vallist = value.split('#')
            value = utils.trim(vallist.pop(0))
        else:
            pass

        try:
            if value[-1] != ';':
                vallist = list(value)
                vallist.append(';')
                value = ''.join(vallist)
                
            if '\\;' in value:
                value = value.replace('\\;', '\\semicolon')

            commandlist: list = value.split(';')
            commandlist.pop(-1)

            for command in commandlist:
                command = utils.trim(command)
                if '$' in command:
                    alias_cmd: list = command.split('$')
                    emp_list: list = []
                    for x in alias_cmd:
                        if ' ' not in x and x:
                            possible_macro = self.aliases.get(x, x)
                            x = possible_macro
                        emp_list.append(x)
                    command = ''.join(emp_list)
                if ';' in command:
                    for x in command.split(';'):
                        if '\\semicolon' in command:
                            command = command.replace('\\semicolon', ';')
                        self.executor(utils.trim(x))
                        continue
                else:
                    if '\\semicolon' in command:
                        command = command.replace('\\semicolon', ';')
                    self.executor(command)
        except IndexError:
            pass

    def executor(self, command: str):
        cmd_split: list = command.split()
        cmd_split_quoted = utils.split_and_quote(' ', '"', command)

        verb: str = cmd_split[0].lower()

        if verb == "banner":
            self.exit_code = banner.run()

        elif verb == 'help':
            if not utils.args(cmd_split, 1):
                Data = PromptHelp('')
                self.exit_code = Data.showHelp()
            else:
                Data = PromptHelp(utils.args(cmd_split, 1))
                self.exit_code = Data.showHelp()

        elif verb == 'led':
            init_editor = start_editor(cmd_split)
            init_editor.start_led()

        elif verb == 'list':
            self.exit_code = aboutList.moduleHelp(self.MODULE).listmodules()

        elif verb == 'show':
            if utils.args(cmd_split, 1):
                if utils.args(cmd_split, 1) == 'options':
                    options = Options(self.MODULE, self.option_dict, _modules)
                    options.showOptions() if utils.args(cmd_split, 2) in ['-t', '--true'] else options.showOptions(False)
                    self.exit_code = 0

                elif utils.args(cmd_split, 1) == 'info':
                    info = Info(self.MODULE)
                    self.exit_code = info.showInfo()

                else:
                    print(f'{FALERT}[-] Error: Invalid argument provided')
                    self.exit_code = 1
            else:
                print(f'{FALERT}[-] Error: no argument provided')
                self.exit_code = 1

        elif verb == 'back':
            if self.MODULE == '':
                raise ExitException(f'{FALERT}probeKit: exiting session')
            else:
                self.MODULE = ''
                self.exit_code = 0

        # Create an exception which exits the try block and then exits the session
        elif verb == 'exit':
            raise ExitException(f'{FALERT}probeKit: exiting session{FNORMAL}')

        elif verb == 'clear':
            if 'Windows' in platform.platform():
                os.system('cls')
                self.exit_code = 0
            else:
                print(chr(27)+'2[j')
                print('\033c')
                print('\x1bc')
                self.exit_code = 0

            if utils.args(cmd_split, 1) == '-e':
                sys.exit(self.exit_code)

        elif verb == 'run':
            self.exit_code = run.run(self.MODULE, self.option_dict)

        # Verb(or command) to set options
        elif verb == 'set':
            new_set  = setval.set_class(self.option_dict, cmd_split[1::])
            ret_list = new_set.run()
            self.option_dict = ret_list[0]
            self.exit_code = ret_list[1]

        # Verb(or command) to unset options
        elif verb == 'unset':
            new_unset = unset.unset_val(self.option_dict, cmd_split[1::])
            ret_list = new_unset.run()
            self.option_dict = ret_list[0]
            self.exit_code = ret_list[1]

        elif verb == 'use':
            new_use = use.use(cmd_split[1::])
            ret_list = new_use.run()
            self.MODULE = ret_list[0]
            self.exit_code = ret_list[1]

        elif verb == 'about':
            if utils.args(cmd_split, 1):
                mod = utils.args(cmd_split, 1)
                aboutList.moduleHelp(mod).aboutModule(mod)
            else:
                aboutList.moduleHelp(self.MODULE).aboutModule(self.MODULE)

        elif verb == 'alias':
            new_alias = alias.alias(cmd_split, self.aliases)
            ret_list = new_alias.run()
            self.aliases = ret_list[0]
            self.exit_code = ret_list[1]

        elif verb == 'unalias':            
            new_unalias = unalias.unalias(self.aliases, cmd_split[1::])
            ret_list = new_unalias.run()
            self.aliases = ret_list[0]
            self.exit_code = ret_list[1]

        elif verb in ['cd', 'chdir', 'set-location']:
            fpath = utils.args(cmd_split, 1)
            if os.path.exists(fpath) and os.path.isdir(fpath):
                os.chdir(fpath)
                print(f'dir: {fpath}')

            else:
                print(f'{FALERT}[-] Error: no such directory: \'{fpath}\'')

        else:
            try:
                if not utils.isAdmin():
                    if 'Windows' not in platform.platform():
                        self.exit_code = subprocess.call((cmd_split_quoted))

                    else:
                        self.exit_code = subprocess.run(command, shell=True).returncode
                        
                else:
                    print(f'{FALERT}Error: Invalid command \'{verb}\'')
                    self.exit_code = 1
                        
            except FileNotFoundError:
                print(f'{FALERT}Error: Invalid command \'{verb}\'')
                self.exit_code = 1

    def main(self):
        check: int = 1 if utils.args(sys.argv, 1) else 0

        readline.set_completer(completer.completion)
        readline.parse_and_bind("tab: complete")

        # Initial module is set to blank
        # Set it to any other module if you want a default module at startup

        if self.MODULE in _modules or self.MODULE == '':
            pass
        else:
            print(f'{FALERT}[-] No such module: \'{self.MODULE}\'{FNORMAL}')
            sys.exit(1)

        try:
            while(True):
                if self.exit_code == 0:
                    COLOR = colors.FSUCCESS
                elif self.exit_code == 3:
                    COLOR = colors.FURGENT
                else:
                    COLOR = colors.FALERT
            
                if check == 0:
                    if self.MODULE == '':
                        prompt_str: str = f'{FNORMAL}[probkit]: {COLOR}{self.exit_code}{FNORMAL}$> '
                    else:
                        prompt_str: str = f'{FNORMAL}probeKit: {FSTYLE}[{self.MODULE}]: {COLOR}{self.exit_code}{FNORMAL}$> '

                    value = input(prompt_str)

                else:
                    value = ' '.join(sys.argv[1].split('\ '))
                    check = 0

                if value:
                    self.parser(value)
                    if 'Windows' not in platform.platform():
                        hist = utils.register_history(value)
                        hist.write_history()

        except EOFError:
            print()
            pass
    
        except KeyboardInterrupt:
            self.exit_code = 130
            print('\n')
            self.main()

        except ExitException as e:
            print(e)
            utils.Exit(self.exit_code) if 'Windows' in platform.platform() else utils.Exit(self.exit_code, histfile)

if __name__ == '__main__':
    new_parser = input_parser()
    new_parser.main()