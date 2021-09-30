from config import colors as _colors
from modules.util.utils import split_and_quote, args

class alias:
    def __init__(self, get_cmd: list, aliases: dict):
        self.get_cmd = get_cmd
        self.aliases = aliases
        
    def run(self):
        tmp_cmd_split = self.get_cmd
        tmp_cmd_split.pop(0)
        new_str = ' '.join(tmp_cmd_split)
        tmp_str = split_and_quote('<', new_str)
        new_alias = args(tmp_str, 0)
        new_cmd = args(tmp_str, 1)
        return self.assign(self.aliases, new_alias, new_cmd)


    def assign(self, aliases: dict= None, alias: str=None, command: str=None) -> list:
        ret_list: list = [{}, 0]

        if bool(command) ^ bool(alias):
            print(f'{_colors.FALERT}Error: required value missing: {_colors.FNORMAL}')
            print(f'command: {bool(command)}')
            print(f'alias:   {bool(alias)}')
            ret_list[1] = 1

        elif not (command and alias):
            ret_list[1] = 0
            for x in aliases:
                print(x,":",aliases[x])
        
        else:
            print(alias, ":",command)
            aliases[alias]=command
            ret_list[1] = 0
        
        return ret_list