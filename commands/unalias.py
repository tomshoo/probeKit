from config import colors as _colors
from rich.console import Console
from typing import List, Union

Console = Console()
_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class unalias:
    def __init__(self, aliases: dict ,alias_list: list):
        self.alias_list = alias_list
        self.ret_list = [aliases, 0]

    def run(self) -> List[Union[dict, int]]:
        if not self.alias_list:
            self.ret_list[1] = 1
            Console.print(f'[{_FALERT}][-] Error: no input provided[/]')
            return self.ret_list

        for alias in self.alias_list:
            self.unassign(alias)

        return self.ret_list

    def unassign(self, alias: str) -> None:
        exit_code: int = self.ret_list[1]
        aliases: dict = self.ret_list[0]

        if alias in aliases:
            del(aliases[alias])
            exit_code = 0

        else:
            Console.print(f'[{_FALERT}\[-] Error: no such alias \'[{_FURGENT}]{alias}[/]\' exists[/]')
            exit_code = 1

        self.ret_list[0] = aliases
        self.ret_list[1] = exit_code
