from config import colors_rich as _colors
from modules.util.utils import split_and_quote, args, trim
from rich import traceback, console
traceback.install()
Console = console.Console()

class alias:
    def __init__(self, get_cmd: list, aliases: dict):
        self.ret_list: list = [aliases, 0]
        self.get_cmd = get_cmd
        self.aliases = aliases

    def run(self) -> list:
        tmp_cmd_split = self.get_cmd
        tmp_cmd_split.pop(0)
        new_str = ' '.join(tmp_cmd_split)
        tmp_str = split_and_quote('<', '"', new_str)
        new_alias = args(tmp_str, 0)
        new_cmd = args(tmp_str, 1)
        self.assign(new_alias, new_cmd)
        return self.ret_list


    def assign(self, alias: str=None, command: str=None) -> list:
        ret_list: list = self.ret_list
        aliases = self.ret_list[0]
        exit_code = self.ret_list[1]

        if bool(command) ^ bool(alias):
            check_c: str = 'x' if bool(command) else '?'
            check_a: str = 'x' if bool(alias) else '?'
            Console.print(f'[{_colors.FALERT}]Error: required value missing: [/]')
            print(f'command: {check_c}')
            print(f'alias:   {check_a}')
            exit_code = 1

        elif not (command and alias):
            exit_code = 0
            for x in aliases:
                print(x,":",aliases[x])

        else:
            alias = trim(alias)
            command = trim(command)
            print(alias, ":",command)
            aliases[alias]=command
            ret_list[1] = 0

        self.ret_list[0] = aliases
        self.ret_list[1] = exit_code