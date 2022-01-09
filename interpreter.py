#!/usr/bin/env python3

# Imports
import sys
import readline
import platform
import os
import argparse
import subprocess
import re

import modules.util.utils as utils
from rich import traceback, console
traceback.install()
Console = console.Console()

if not ('-h' in sys.argv or '--help' in sys.argv):
    print(f'Importing custom modules', end='\r')
start = utils.timefunc.timestamp()

import modules.data.AboutList as aboutList
from commands import (
    run, set as setval, unset,
    alias, unalias, use,
    banner, show, clear
)
from modules.data import Help
from config import (
    MODULE, colors, aliases,
    option_dict, valid_modules as _modules
)
from modules.util.led import start_editor

end = utils.timefunc.timestamp()
if not ('-h' in sys.argv or '--help' in sys.argv):
    Console.print(f'[{colors.FSUCCESS}]modules took {round(end-start, 7)} sec(s). to load[/]')

class SudoError(Exception): pass

# Setup Utils
optionparser = utils.optionsparser(option_dict)
option_dict = optionparser.parse()
ExitException = utils.ExitException
completer = utils.completer(utils.completers.interpreter)

# Setting up colors (edit these in config.py)
FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FURGENT = colors.FURGENT
FSTYLE = colors.FPROMPT

# Display time during statup
if not ('-h' in sys.argv or '--help' in sys.argv):
    print(f'current session started at {utils.timefunc.datevalue()}')

if utils.args(sys.argv, 1) in ['-h', '--help']:
    banner.run()
    print()

parser = argparse.ArgumentParser(description="Command line toolkit for basic reconnaisance")
parser.add_argument('-c', '--command', help='custom command to run from outside the session')
parser.add_argument('-m', '--module', help="Start with a specified module (Overrides default module set in config)")
parser.add_argument('-q', '--quiet', help="Do not display banner on startup", action='store_true')

args = parser.parse_args()

if not args.quiet:
    banner.run()
    
if args.module and args.module not in _modules:
    Console.print(f'[{FALERT}]Alert: Invalid module `{args.module}`, defaulting to no module[/]')

# Checks if history file already exists or not
if 'Windows' not in platform.platform():
    histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')
    if os.path.exists(histfile): readline.read_history_file(histfile)

if not utils.isAdmin():
    Console.print(f'[{FURGENT}]Warning: `osprobe` and `UDP Scanning` may not work as expected...')

# Session starts over here
# Not the best way to do it but it works so...

class input_parser:

    def __init__(self):
        self.exit_code: int = 0
        # Variables also known as options to the user
        self.option_dict: dict = option_dict

        self.MODULE: str = MODULE if not args.module or args.module not in _modules else args.module
        self.MODLIST: list = []
        self.aliases: dict = aliases

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
                
            if '\\;' in value: value = value.replace('\\;', '\\semicolon')

            # commandlets: list = re.findall('\{.*?\}', value)
            commandlets: list = utils.splitters().bracket(value, '{')
            if commandlets is None:
                self.exit_code = 3
                return
            cmdletdict: dict = {}

            for idx, commandlet in enumerate(commandlets):
                cmdletdict['cmdlet_'+str(idx)] = commandlet
            for replacer in cmdletdict:
                value = value.replace('{'+cmdletdict.get(replacer)+'}', replacer)

            commandlist: list = utils.splitters.dbreaker(value, delimiter=';')

            for command in commandlist:
                command = utils.trim(command)
                if not command:
                    continue
                #print (re.findall('\{.*?\}', command))
                if '$' in command:
                    alias_cmd: list = command.split('$')
                    emp_list: list = []
                    for x in alias_cmd:
                        if ' ' not in x and x:
                            possible_macro = self.aliases.get(x, x)
                            x = possible_macro
                        emp_list.append(x)
                    command = ''.join(emp_list)
                    print(command)
                if ';' in command:
                    for x in utils.splitters.dbreaker(command, delimiter=';'):
                        if '\\semicolon' in command:
                            command = command.replace('\\semicolon', ';')
                        for cmdlet_idx in cmdletdict:
                            command = command.replace(cmdlet_idx, cmdletdict.get(cmdlet_idx).replace(' ', '_'))
                        self.executor(utils.trim(x))
                        continue
                else:
                    if '\\semicolon' in command:
                        command = command.replace('\\semicolon', ';')
                    for cmdlet_idx in cmdletdict:
                        command = command.replace(cmdlet_idx, cmdletdict.get(cmdlet_idx).replace(' ', '_'))
                    self.executor(command)
        except IndexError:
            pass

    def executor(self, command: str):
        cmd_split: list = command.split()
        # cmd_split_quoted = utils.splitters.quote(' ', '"', command)
        cmd_split_quoted = utils.splitters.quote(command, ' ')

        verb: str = cmd_split[0].lower()

        if verb == "banner":
            self.exit_code = banner.run()

        elif verb == 'do':
            try:
                times: int = 1
                if ('-t' in command):
                    argument: str = ''
                    check: int = 0
                    times = command[command.find('-t')+3]
                noreturn: bool = True if '-n' in command else False
                self.do(cmd_split[1], int(times), noreturn)
                pass
            except ValueError:
                Console.print(f'[{FALERT}]Error: Invalid argument[/]')

        elif verb == 'help':
            if not utils.args(cmd_split, 1):
                Data = Help.Help('')
                self.exit_code = Data.showHelp()
            else:
                Data = Help.Help(utils.args(cmd_split, 1))
                self.exit_code = Data.showHelp()

        elif verb == 'led':
            init_editor = start_editor(cmd_split)
            init_editor.start_led()

        elif verb == 'show':
            self.exit_code = show.run(cmd_split[1::], self.MODULE, self.option_dict)

        elif verb == 'back':
            if not self.MODULE:
                Console.print(f'[{FURGENT}]Alert: No module selected... nothing to back from.')
            else:
                if self.MODULE == (self.MODLIST[-1] if self.MODLIST else None):
                    try:
                        self.MODLIST.pop()
                    except Exception as e:
                        print(e)
                else:
                    pass

                self.MODULE = self.MODLIST.pop() if self.MODLIST else ''

        # Create an exception which exits the try block and then exits the session
        elif verb == 'exit':
            if utils.args(cmd_split, 1) == '-q':
                raise ExitException()
            else:
                raise ExitException(f'probeKit: exiting session')

        elif verb == 'clear':
            self.exit_code = clear.run(cmd_split[1::], self.exit_code, histfile) if 'Windows' not in platform.platform() else clear.run(cmd_split[1::], self.exit_code)

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
            new_use = use.use(cmd_split[1::], self.MODLIST)
            ret_list = new_use.run()
            self.MODLIST = ret_list[0]
            self.MODULE = self.MODLIST[-1]
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
                self.exit_code = 0

            else:
                Console.print(f'[{FALERT}][-] Error: no such directory: \'{fpath}\'[/]')
                self.exit_code = 1

        else:
            PATH: list=(os.getenv('PATH')+':').split(':')
            for path in PATH:
                try:
                    with open(path+'/'+verb, 'r') if 'Windows' not in platform.platform() else open(path+'\\'+verb) as cmd:
                        content = cmd.read()
                except UnicodeDecodeError:
                    pass
                except FileNotFoundError:
                    pass
                else:
                    if len(re.findall('sudo*', content)) > 0 or 'sudo' in content:
                        Console.print(f'[{FALERT}]Warning: sudo found in script, not running...')
                        raise SudoError()
            if verb.lower() == 'sudo':
                Console.print(f'[{FALERT}]Warning: using sudo is prohibited for security reasons[/]')
                raise SudoError()
            try:
                if not utils.isAdmin():
                    if 'Windows' not in platform.platform():
                        self.exit_code = subprocess.call((cmd_split_quoted))
                    else:
                        self.exit_code = subprocess.run(command, shell=True).returncode
                        
                else:
                    Console.print(f'[{FALERT}]Error: Invalid command \'{verb}\'[/]')
                    self.exit_code = 1

            except FileNotFoundError:
                Console.print(f'[{FALERT}]Error: Invalid command \'{verb}\'[/]')
                self.exit_code = 1

    def prompt(self, check: int = 0) -> int:
        if self.exit_code == 0:
            COLOR: str = colors.FSUCCESS
        elif self.exit_code == 130:
            COLOR: str = colors.FURGENT
        else:
            COLOR: str = colors.FALERT

        if not self.MODULE:
            prompt_str: str = f'\[probkit]: [{COLOR}]{self.exit_code}[/]$> '
        else:
            prompt_str: str = f'\[probeKit]: [{FSTYLE}]({self.MODULE})[/]: [{COLOR}]{self.exit_code}[/]$> '
        if check == 0:
            value = Console.input(prompt_str)
        else:
            external_command: str = args.command
            splitted: list = external_command.split('\ ')
            splitted.append(';exit -q')
            value = ' '.join(splitted); check = 0

        if value:
            value = utils.trim(value)
            if value[-1] == '\\':
                concatinator: list = [value[:-1]]
                while(True):
                    line: str = input('..> ')
                    if not line: break
                    concatinator.append(line)
                value = ''.join(concatinator)
            self.parser(value)
            if 'Windows' not in platform.platform():
                hist = utils.register_history(value)
                hist.write_history()
        return 0

    def main(self):
        check: int = 1 if args.command else 0

        readline.set_completer(completer.completion)
        readline.parse_and_bind("tab: complete")

        # Initial module is set to blank
        # Set it to any other module if you want a default module at startup

        if self.MODULE in _modules or self.MODULE == '':
            pass
        
        else:
            Console.print(f'[{FALERT}][-] No such module: [bold underline]\'{self.MODULE}\'[/][/]')
            sys.exit(1)

        try:
            while(True):
                check = self.prompt(check)

        except EOFError:
            print()
            pass
    
        except KeyboardInterrupt:
            self.exit_code = 130
            print('\n')
            self.main()

        except SudoError:
            self.exit_code = 1
            self.main()

        except ExitException as e:
            Console.print(f"[{FALERT}]"+e.__str__()+"[/]")
            utils.Exit(self.exit_code) if 'Windows' in platform.platform() else utils.Exit(self.exit_code, histfile)

    def do(self, command: str, times: int = 1, noreturn: bool = False) -> int:
        command = command.replace('_', ' ')
        if noreturn:
            try:
                for x in range(times):
                    self.parser(command)
            except Exception as e:
                print(e)
            self.exit_code = 0
        else:
            for x in range(times):
                self.parser(command)
        pass

if __name__ == '__main__':
    new_parser = input_parser()
    new_parser.main()