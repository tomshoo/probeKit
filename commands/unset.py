from config import colors as _colors, default_command_dict
from modules.util import optparser
from modules.util.extra import get_args
from modules.util.CommandUtils.ReturnStructure import RetObject
from modules.data.Help import Help
from rich.console import Console
# from fuzzywuzzy import fuzz

console = Console()
_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT


class unset_val:
    def __init__(self, arguemnts: list[str], ReturnObject: RetObject):
        self.args: list[str] = arguemnts
        self.retobj = ReturnObject

    def run(self) -> RetObject:
        if not self.args:
            self.retobj.exit_code = 1
            return self.retobj

        if "-h" in (l := [a.lower() for a in self.args]) or "--help" in l:
            self.retobj.exit_code = Help("set").showHelp()
            return self.retobj

        if not [x for x in ["option", "alias", "macro"] if x == self.args[0].lower()]:
            console.print(f"[{_FALERT}]Error: Not a valid action")
            self.retobj.exit_code = 1
            return self.retobj

        if (func := {
            "option": self.unassign_option,
            "alias": self.unassign_alias,
            "macro": self.unassign_macro
        }.get(self.args[0].lower())) is not None:
            if (k := get_args(self.args, 1) is not None) and k == "all":
                if func == self.unassign_macro:
                    self.retobj.macros = {}
                elif func == self.unassign_alias:
                    self.retobj.aliases = {}
                else:
                    for item in self.retobj.option_dict:
                        func(item)
                return self.retobj

            for key in self.args[1:]:
                func(key)
            pass
        return self.retobj

    def unassign_option(self, option: str):
        options_dict: dict = self.retobj.option_dict
        if options_dict.get(option):
            if options_dict[option]["type"] != "dict":
                options_dict[option]["value"] = ""
            else:
                options_dict[option]["value"]["value"] = ""
                options_dict[option]["value"]["type"] = ""

        else:
            console.print(f"[{_FALERT}]Error: invalid option '{option}'[/]")
            self.retobj.exit_code = 1
            return

        parser = optparser.OptionsParser(options_dict)
        options_dict = parser.parse()
        console.print(f"[{_FURGENT}]unset {option}[/]")
        self.retobj.option_dict = options_dict
        self.retobj.exit_code = 0

    def unassign_alias(self, alias: str) -> None:
        aliases: dict = self.retobj.aliases

        if aliases.get(alias):
            if default_command_dict.get(alias):
                self.retobj.aliases[alias] = default_command_dict[alias]
                self.retobj.exit_code = 0
                return
            print(alias)
            del aliases[alias]
            self.retobj.exit_code = 0

        else:
            console.print(
                f"[{_FALERT}][-] Error: no such alias '[{_FURGENT}]{alias}[/]' exists[/]"
            )
            self.retobj.exit_code = 2

        self.retobj.aliases = aliases

    def unassign_macro(self, macro: str) -> None:
        macros: dict = self.retobj.macros

        if macro in macros:
            print(macro)
            del macros[macro]
            self.retobj.exit_code = 0

        else:
            console.print(
                f"[{_FALERT}][-] Error: no such alias '[{_FURGENT}]{macro}[/]' exists[/]"
            )
            self.retobj.exit_code = 2

        self.retobj.aliases = macros
