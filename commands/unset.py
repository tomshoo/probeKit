from config import colors as _colors
from modules.util import optparser, splitters
from modules.util.extra import args
from modules.data.Help import Help
from rich.console import Console
from typing import List, Union

Console = Console()
_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class unset_val:
    def __init__(self, args: str, option_dict: dict[str], aliases: dict[str]):
        self.aliases = aliases
        self.option_dict = option_dict
        self.exit_code: int = 0
        self.args: list[str] = splitters.Splitters().dbreaker(args)

    def run(self) -> List[Union[dict, int]]:
        if len(self.args) < 1 or not args(self.args, 0):
            Console.print(f'[{_FALERT}]Error: unset type was not found or was invalid[/]')
            return [self.option_dict, self.aliases, 1]

        elif '-h' in [x.lower() for x in self.args] or '--help' in [x.lower() for x in self.args]:
            Help('unset').showHelp()
            return [self.option_dict, self.aliases, self.exit_code]
            
        elif args(self.args, 0).lower() in ['option', 'alias']:
            if self.args[0].lower() == 'option':
                unassignment_func = self.unassign_option
            else:
                unassignment_func = self.unassign_alias
        else:
            Console.print(f'[{_FALERT}]Error: unset type was invalid required: \'option\' (or) \'alias\', found: {self.args[0]}[/]')
            return [self.option_dict, self.aliases, 1]

        keylist: list[str] = self.args[1::]

        if 'all' in [x.lower() for x in keylist]:
            if unassignment_func == self.unassign_option:
                for key in self.option_dict:
                    unassignment_func(key)
            else:
                temp_dict = self.aliases.copy()
                for key in temp_dict:
                    unassignment_func(key)
                del temp_dict

        else:
            for key in keylist:
                unassignment_func(key)

        return [self.option_dict, self.aliases, self.exit_code]

    def unassign_option(self, option: str):
        options_dict: dict = self.option_dict
        if options_dict.get(option):
            if options_dict[option]['type'] != "dict": options_dict[option]['value'] = ""
            else:
                options_dict[option]['value']['value'] = ""
                options_dict[option]['value']['type'] = ""

        else:
            Console.print(f'[{_FALERT}]Error: invalid option \'{option}\'[/]')
            self.exit_code
            return

        parser = optparser.OptionsParser(options_dict)
        options_dict = parser.parse()
        Console.print(f'[{_FURGENT}]unset {option}[/]')
        self.option_dict = options_dict
        self.exit_code = 0


    def unassign_alias(self, alias: str) -> None:
        aliases: dict = self.aliases

        if alias in aliases:
            print(alias)
            del(aliases[alias])
            self.exit_code = 0

        else:
            Console.print(f'[{_FALERT}\[-] Error: no such alias \'[{_FURGENT}]{alias}[/]\' exists[/]')
            self.exit_code = 2

        self.aliases = aliases