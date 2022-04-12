#!/usr/bin/env python3

# Imports
import sys
import readline
import platform
import os
import argparse
import subprocess
import re
from fuzzywuzzy import process
from modules.util.CommandUtils.CommandStruct import CreateCommand

from modules.util import splitters, extra, optparser, hist as history
from rich import traceback, console
traceback.install()
Console = console.Console(soft_wrap=True, highlight=False)

if not ('-h' in sys.argv or '--help' in sys.argv):
    print(f'Importing custom modules', end='\r')

start = extra.timefunc.timestamp()

import modules.data.AboutList as aboutList
from commands import banner
from config import (
    MODULE, colors, aliases, macros,
    option_dict, valid_modules as _modules
)
from modules.util.led import start_editor

end = extra.timefunc.timestamp()

if not ('-h' in sys.argv or '--help' in sys.argv):
    Console.print(f'[{colors.FSUCCESS}]modules took {round(end-start, 7)} sec(s). to load[/]')

class SudoError(Exception): pass
splitter = splitters.Splitters()

# Setup Utils
optionparser = optparser.OptionsParser(option_dict)
option_dict = optionparser.parse()
ExitException = extra.ExitException
completer = extra.completer(extra.completers.interpreter)

# Setting up colors (edit these in UserConfig.py)
FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FURGENT = colors.FURGENT
FSTYLE = colors.FPROMPT

# Display time during statup
if not ('-h' in sys.argv or '--help' in sys.argv or '-l' in sys.argv or '--list' in sys.argv):
    print(f'current session started at {extra.timefunc.datevalue()}')

if extra.args(sys.argv, 1) in ['-h', '--help']:
    banner.paint()
    print()

parser = argparse.ArgumentParser(description="Command line toolkit for basic reconnaisance")
parser.add_argument('-c', '--command', help='custom command to run from outside the session')
parser.add_argument('-m', '--module', help="Start with a specified module (Overrides default module set in config)")
parser.add_argument('-q', '--quiet', help="Do not display banner on startup", action='store_true')
parser.add_argument('-l', '--list', help="list available modules", action="store_true")

args = parser.parse_args()

if args.list:
    Console.print(f"[{FSUCCESS}]Available module are:")
    for module in _modules:
        Console.print(f'\t-> [{FURGENT}]{module}[/]')
    print()
    sys.exit(0)


if not args.quiet:
    banner.paint()
    
if args.module and args.module not in _modules:
    Console.print(f'[{FALERT}]Alert: Invalid module `{args.module}`, defaulting to no module[/]')

# Checks if history file already exists or not
if 'Windows' not in platform.platform():
    histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')
    if os.path.exists(histfile): readline.read_history_file(histfile)
else:
    histfile = None

if not extra.isAdmin():
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
        self.macros: dict = macros

    def parser(self, value: str):
        if '#' in value:
            vallist = value.split('#')
            value = extra.trim(vallist.pop(0))
        else:
            pass

        try:
            if value[-1] != ';':
                vallist = list(value)
                vallist.append(';')
                value = ''.join(vallist)
                
            if '\\;' in value: value = value.replace('\\;', '\\semicolon')

            # commandlets: list = re.findall('\{.*?\}', value)
            commandlets: list = splitter.bracket(value, '{')
            if commandlets is None:
                self.exit_code = 3
                return
            cmdletdict: dict = {}

            for idx, commandlet in enumerate(commandlets):
                cmdletdict['cmdlet_'+str(idx)] = commandlet
            for replacer in cmdletdict:
                value = value.replace('{'+cmdletdict.get(replacer)+'}', replacer)

            commandlist: list = splitter.dbreaker(value, delimiter=';')

            for command in commandlist:
                command = extra.trim(command)
                if not command:
                    continue
                
                is_alias: bool = True if aliases.get(command.split()[0]) else False
                while is_alias:
                    token = command.split()[0]
                    if aliases.get(token):
                        if aliases.get(token)[0].split()[0] == token:
                            is_alias = False
                            break
                        command = command.replace(token, aliases.get(token, [token])[0], 1)
                    else:
                        is_alias = False
                command = command.replace(command.split()[0], aliases.get(command.split()[0], [command.split()[0]])[0], 1)
                if '$' in command:
                    for x in re.findall('\$\(.*?\)', command):
                        command = command.replace(x, macros.get(x[2:-1:], x[2:-1:]))
                    cmd_list = command.split(' ')
                    for x in cmd_list:
                        if x.strip('"').strip('\'').startswith('$'):
                            command=command.replace(x, macros.get(x.strip('$'), ''))
                    cmd_list=command.split('=')
                    for x in cmd_list:
                        if x.strip('"').strip('\'').strip().startswith('$'):
                            command=command.replace(x, macros.get(x.strip('$'), ''))
                    print(command)
                if ';' in command:
                    for x in splitter.dbreaker(command, delimiter=';'):
                        if '\\semicolon' in command:
                            command = command.replace('\\semicolon', ';')
                        for cmdlet_idx in cmdletdict:
                            command = command.replace(cmdlet_idx, cmdletdict.get(cmdlet_idx).replace(' ', '_'))
                        self.executor(extra.trim(x))
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
        arglist = command.split(' ')
        arglist.pop(0)
        arguments = ' '.join(arglist)
        cmd_split: list = command.split()
        cmd_split_quoted = splitter.quote(command, ' ')

        verb: str = cmd_split[0].lower()

        CommandStruct = CreateCommand(
                arguments=splitter.dbreaker(arguments),
                option_dict=self.option_dict,
                aliases=self.aliases,
                macros=self.macros,
                activated_module_list=self.MODLIST,
                module=self.MODULE,
                histfile=histfile
        ).run(verb)

        if CommandStruct.command_found:
            self.option_dict = CommandStruct.option_dict
            self.aliases = CommandStruct.aliases
            self.macros = CommandStruct.macros
            self.MODLIST = CommandStruct.activated_module_list
            self.MODULE = CommandStruct.module
            self.exit_code = CommandStruct.exit_code

        elif verb == 'do':
            try:
                times: int = 1
                if ('-t' in command):
                    times = command[command.find('-t')+3]
                noreturn: bool = True if '-n' in command else False
                self.do(cmd_split[1], int(times), noreturn)
                pass
            except ValueError:
                Console.print(f'[{FALERT}]Error: Invalid argument[/]')

        elif verb == 'led':
            init_editor = start_editor(cmd_split)
            init_editor.start_led()

        # Create an exception which exits the try block and then exits the session
        elif verb == 'exit':
            if extra.args(cmd_split, 1) == '-q':
                raise ExitException()
            else:
                raise ExitException(f'probeKit: exiting session')

        elif verb == 'about':
            if extra.args(cmd_split, 1):
                mod = extra.args(cmd_split, 1)
                aboutList.moduleHelp(mod).aboutModule(mod)
            else:
                aboutList.moduleHelp(self.MODULE).aboutModule(self.MODULE)

        elif verb in ['cd', 'chdir', 'set-location']:
            fpath = extra.args(cmd_split, 1)
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
                        content = cmd.read().lower()
                except UnicodeDecodeError:
                    pass
                except FileNotFoundError:
                    pass
                else:
                    if max(len(re.findall('sudo*', content)), len(re.findall('gsudo', content))) > 0 or 'sudo' in content or 'gsudo' in content:
                        Console.print(f'[{FALERT}]Warning: sudo or gsudo found in script, not running...')
                        raise SudoError()
            if verb.lower() in ['sudo', 'gsudo']:
                Console.print(f'[{FALERT}]Warning: using sudo or gsudo is prohibited for security reasons[/]')
                raise SudoError()
            try:
                if not extra.isAdmin():
                    if 'Windows' not in platform.platform():
                        self.exit_code = subprocess.call((cmd_split_quoted))
                    else:
                        self.exit_code = subprocess.run(command).returncode
                        
                else:
                    Console.print(f'[{FALERT}]Error: Invalid command \'{verb}\'[/]')
                    self.exit_code = 1

            except FileNotFoundError:
                Console.print(f'[{FALERT}]Error: Invalid command \'{verb}\'[/]')
                fuzzy_match_list: list[str] = [x for x in process.extractBests(verb, extra.completers.interpreter)]
                Console.print(f'[{colors.FURGENT}]Perhaps you meant: [/]')
                for match in fuzzy_match_list:
                    Console.print(f'\t[{colors.FPROMPT}]{match[0]}[/]')
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
            value = console.Console(soft_wrap=True).input(prompt_str)
        else:
            external_command: str = args.command
            splitted: list = external_command.split('\ ')
            splitted.append(';exit -q')
            value = ' '.join(splitted); check = 0

        if value:
            value = extra.trim(value)
            if value[-1] == '\\':
                concatinator: list = [value[:-1]]
                while(True):
                    line: str = input('..> ')
                    if not line: break
                    concatinator.append(line)
                value = ''.join(concatinator)
            self.parser(value)
            if 'Windows' not in platform.platform():
                hist = history.register_history(value)
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
            extra.Exit(self.exit_code) if 'Windows' in platform.platform() else extra.Exit(self.exit_code, histfile)

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
            for _ in range(times):
                self.parser(command)
        pass

if __name__ == '__main__':
    new_parser = input_parser()
    new_parser.main()