from config import colors as _colors, OPTIONS
from modules.util.extra import trim, args
from modules.util import optparser
from modules.util.splitters import Splitters
from modules.data.Help import Help
from modules.util.ReturnStructure import RetObject
from rich import console,traceback
from typing import List, Union
from fuzzywuzzy import fuzz
traceback.install()
Console = console.Console()

_FALERT = _colors.FALERT
_FSTYLE = _colors.FPROMPT
_FURGENT = _colors.FURGENT

class Set:
    # def __init__(self, args: str, option_dict: dict[str]=None, aliases: dict[str]=None, macros: dict[str]=None):
    def __init__(self, arguments, ReturnObject: RetObject) -> None:
        self.args = arguments
        self.ReturnObject = ReturnObject

    def run(self) -> RetObject:
        exit_code: int = 0
        temp_arglist = [x.lower() for x in self.args]
        if '-h' in temp_arglist or '--help' in temp_arglist:
            Help('set').showHelp()
            del temp_arglist
            return self.ReturnObject
        if args(self.args, 0).lower() not in ['option', 'alias', 'macro']:
            Console.print(f'[{_FALERT}]Error set type not valid[/]')
            if fuzz.partial_ratio(args(self.args, 0).lower(), "option") > 80:
                Console.print(f'[{_FURGENT}]Did you mean `option`?')
            if fuzz.partial_ratio(args(self.args, 0).lower(), "alias") > 80:
                Console.print(f'[{_FURGENT}]Did you mean `alias`?')
            self.ReturnObject.exit_code = 2
            return self.ReturnObject
        if len(self.args) < 2: 
            Console.print(f'[{_FALERT}]Error: no values to assign[/]')
            self.ReturnObject.exit_code = 3
            return self.ReturnObject
        optlist = self.args[1::]
        if args(self.args, 0).lower() == 'option': assignment_func = self.assign_options
        if args(self.args, 0).lower() == 'alias': assignment_func = self.assign_alias
        if args(self.args, 0).lower() == 'macro':
            if len(optlist) > 1:
                Console.print(f'[{_FALERT}]Error: Defining multiple macros at once is nor supported not recommended.[/]')
                self.ReturnObject.exit_code = 3
            else:
                if '=' not in args(optlist, 0):
                    Console.print(f'[{_FALERT}]What!!? What am I supposed to assign to what again??[/]')
                    self.ReturnObject.exit_code = 3
                else:
                    assignment_list = Splitters.dbreaker(args(optlist, 0), '=')
                    if len(assignment_list) == 2:
                        if not args(assignment_list, 0):
                            Console.print(f'[{_FALERT}]Again... to whom am I supposed to assign the value!![/]')
                            self.ReturnObject.exit_code = 3
                        else:
                            self.ReturnObject.macros[args(assignment_list,0)]=args(assignment_list, 1).strip('"').strip('\'')
                            self.ReturnObject.exit_code = 0
                    else:
                        if len(assignment_list) > 2:
                            Console.print(f'[{_FALERT}]Whoa!!! Don\'t the macro!![/]')
                            self.ReturnObject.exit_code = 3
                        else:
                            Console.print(f'[{_FALERT}]What am I supposed to assignt to this thing!![/]')
                            self.ReturnObject.exit_code = 3

            return self.ReturnObject
        if 'all' in [x.lower() for x in optlist]:
            if assignment_func == self.assign_options:
                for option in self.ReturnObject.option_dict:
                    if OPTIONS.get(option):
                        if self.ReturnObject.option_dict[option]['type'] == "dict":
                            self.ReturnObject.option_dict[option]['value']['value'] = OPTIONS.get(option)
                        else: self.ReturnObject.option_dict[option]['value'] = OPTIONS.get(option)
            else:
                Console.print(f'[{_FALERT}]Error: keyword `all` is not available for alias assignment')
                self.ReturnObject.exit_code = 3
        else:
            for x in optlist:
                if '=' not in x and assignment_func == self.assign_options:
                    if OPTIONS.get(x):
                        self.assign_options(x, OPTIONS.get(x))
                    else:
                        Console.print(f'[{_FALERT}]Error: default value for option `{x}` not found[/]')
                        exit_code = 1
                else:
                    if len(x) == 1:
                        back_value = args(optlist, optlist.index(x)-1) if args(optlist, optlist.index(x)-1) and (optlist.index(x)-1) > 0 else '[]'
                        front_value = args(optlist, optlist.index(x)+1) if args(optlist, optlist.index(x)+1) else '[]'

                        Console.print(f'[{_FALERT}]What!!?? I need a KEY AND VALUE please...[/]')
                        Console.print(f'[{_FALERT}]Go look for your self: > `[{_FSTYLE}]{back_value} >{x}< {front_value}[/]`')
                        exit_code = 3
                    else:
                        assignment_list = Splitters.dbreaker(x, '=')
                        if len(assignment_list) == 1:
                            back_value = args(optlist, optlist.index(x)-1) if args(optlist, optlist.index(x)-1) and (optlist.index(x)-1) > 0 else '[]'
                            front_value = args(optlist, optlist.index(x)+1) if args(optlist, optlist.index(x)+1) else '[]'
                            if back_value == x: back_value = '[]'

                            Console.print(f'[{_FALERT}]AND a VALUE for god\'s sake[/]')
                            Console.print(f'[{_FALERT}]Man!! what a beautiful pair of eyes you have over there: > `[{_FSTYLE}]{back_value} >{x}< {front_value}[/]`')
                            exit_code = 3
                            break
                        elif not args(assignment_list, 0):
                            back_value = args(optlist, optlist.index(x)-1) if args(optlist, optlist.index(x)-1) and (optlist.index(x)-1) > 0 else '[]'
                            front_value = args(optlist, optlist.index(x)+1) if args(optlist, optlist.index(x)+1) else '[]'
                            if back_value == x: back_value = '[]'

                            Console.print(f'[{_FALERT}]What!!!? Where is the KEY...[/]')
                            Console.print(f'[{_FALERT}]Look over here if you are blind: > `[{_FSTYLE}]{back_value} >{x}< {front_value}[/]`')
                            exit_code = 3
                            break
                        else:
                            for idx,data in enumerate(assignment_list):
                                if not data:
                                    assignment_list.pop(idx)
                            assignment_func(assignment_list[0], assignment_list[1])

        if exit_code:
            self.exit_code = exit_code
            exit_code = 0
        return self.ReturnObject

    def assign_options(self, option: str, value: str):
        options = self.ReturnObject.option_dict
        if options.get(option):
            if options[option]['type'] != "dict": options[option]['value'] = value
            else: options[option]['value']['value'] = value
        else:
            Console.print(f'[{_FALERT}]Error: Invalid option \'{option}\'[/]')
            self.ReturnObject.exit_code = 1
            return
        
        parser = optparser.OptionsParser(options)
        options = parser.parse()
        print(option, '=>', value)
        self.ReturnObject.option_dict = options
        self.ReturnObject.exit_code = 0

    def assign_alias(self, alias: str=None, command: str=None) -> list:
        aliases = self.ReturnObject.aliases
        exit_code = self.ReturnObject.exit_code

        alias = trim(alias)
        command = trim(command)
        command = command.strip('"')
        command = command.strip('\'')
        print(alias, ":",command)
        aliases[alias]=command

        self.ReturnObject.aliases = aliases
        self.ReturnObject.exit_code = exit_code