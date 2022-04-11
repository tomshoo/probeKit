from config import colors as _colors, default_command_dict
from modules.util import optparser
from modules.util.extra import args
from modules.util.CommandUtils.ReturnStructure import RetObject
from modules.data.Help import Help
from rich.console import Console
from fuzzywuzzy import fuzz

Console = Console()
_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class unset_val:
    # def __init__(self, args: str, option_dict: dict[str], aliases: dict[str], macros: dict[str]):
    def __init__(self, arguemnts: list[str], ReturnObject: RetObject):
        self.args: list[str] = arguemnts
        self.ReturnObject = ReturnObject

    def run(self) -> RetObject:
        if len(self.args) < 1 or not args(self.args, 0):
            Console.print(f'[{_FALERT}]Error: unset type was not found or was invalid[/]')
            self.ReturnObject.exit_code = 1

        elif '-h' in [x.lower() for x in self.args] or '--help' in [x.lower() for x in self.args]:
            self.ReturnObject.exit_code = Help('unset').showHelp()
            return self.ReturnObject

        elif args(self.args, 0).lower() in ['option', 'alias', 'macro']:
            if self.args[0].lower() == 'option':
                unassignment_func = self.unassign_option
            elif self.args[0].lower() == 'alias':
                unassignment_func = self.unassign_alias
            else:
                unassignment_func = self.unassign_macro
        else:
            Console.print(f'[{_FALERT}]Error: unset type was invalid required: \'option\', \'alias\' (or) \'macro\', found: {self.args[0]}[/]')
            if fuzz.partial_ratio(args(self.args, 0).lower(), "option") > 80:
                Console.print(f'[{_FURGENT}]Did you mean `option`?')
            elif fuzz.partial_ratio(args(self.args, 0).lower(), "alias") > 80:
                Console.print(f'[{_FURGENT}]Did you mean `alias`?')
            elif fuzz.partial_ratio(args(self.args, 0).lower(), "macro") > 80:
                Console.print(f'[{_FURGENT}]Did you mean `macro`?')
            self.ReturnObject.exit_code = 2
            return self.ReturnObject

        keylist: list[str] = self.args[1::]

        if 'all' in [x.lower() for x in keylist]:
            if unassignment_func == self.unassign_option:
                for key in self.ReturnObject.option_dict:
                    unassignment_func(key)
            elif unassignment_func == self.unassign_alias:
                self.ReturnObject.aliases = {}
            else:
                self.ReturnObject.macros = {}


        else:
            if [x for x in keylist if '=' in x]:
                self.ReturnObject.exit_code = 3
                Console.print(f'[{_FALERT}]Error: cannot assign values in unset command[/]')
            else:
                for key in keylist:
                    unassignment_func(key)

        return self.ReturnObject

    def unassign_option(self, option: str):
        options_dict: dict = self.ReturnObject.option_dict
        if options_dict.get(option):
            if options_dict[option]['type'] != "dict": options_dict[option]['value'] = ""
            else:
                options_dict[option]['value']['value'] = ""
                options_dict[option]['value']['type'] = ""

        else:
            Console.print(f'[{_FALERT}]Error: invalid option \'{option}\'[/]')
            self.ReturnObject.exit_code = 1
            return

        parser = optparser.OptionsParser(options_dict)
        options_dict = parser.parse()
        Console.print(f'[{_FURGENT}]unset {option}[/]')
        self.ReturnObject.option_dict = options_dict
        self.ReturnObject.exit_code = 0


    def unassign_alias(self, alias: str) -> None:
        aliases: dict = self.ReturnObject.aliases

        if aliases.get(alias):
            if default_command_dict.get(alias):
                self.ReturnObject.aliases[alias] = default_command_dict[alias]
                print(aliases)
                self.ReturnObject.exit_code = 0
                return
            print(alias)
            del(aliases[alias])
            self.ReturnObject.exit_code = 0

        else:
            Console.print(f'[{_FALERT}][-] Error: no such alias \'[{_FURGENT}]{alias}[/]\' exists[/]')
            self.ReturnObject.exit_code = 2

        self.ReturnObject.aliases = aliases
    def unassign_macro(self, macro: str) -> None:
        macros: dict = self.ReturnObject.macros

        if macro in macros:
            print(macro)
            del(macros[macro])
            self.ReturnObject.exit_code = 0

        else:
            Console.print(f'[{_FALERT}][-] Error: no such alias \'[{_FURGENT}]{macro}[/]\' exists[/]')
            self.ReturnObject.exit_code = 2

        self.ReturnObject.aliases = macros