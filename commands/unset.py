from config import colors as _colors
from modules.util import optparser
from modules.data.Help import Help
from rich.console import Console
from typing import List, Union

Console = Console()
_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class unset_val:
    def __init__(self, option_dict: dict[str], options: list[str]):
        ret_list = [option_dict, 0]
        self.ret_list = ret_list
        self.options = options

    def run(self) -> List[Union[dict, int]]:
        options = [x.lower() for x in self.options]
        if '-h' in options or '--help' in options:
            return [self.ret_list[0], Help('unset').showHelp()]
        for option in options: self.unassign(option)
        return self.ret_list

    def unassign(self, option: str):
        options_dict: dict = self.ret_list[0]
        option = option.upper()
        if option.lower() == "all":
            for data in options_dict:
                if options_dict[data]['type'] == "dict":
                    options_dict[data]['value']['value'] = ""
                    options_dict[data]['value']['type'] = ""
                else: options_dict[data]['value'] = ""

        elif options_dict.get(option):
            if options_dict[option]['type'] != "dict": options_dict[option]['value'] = ""
            else:
                options_dict[option]['value']['value'] = ""
                options_dict[option]['value']['type'] = ""

        else:
            Console.print(f'[{_FALERT}]Error: invalid option \'{option}\'[/]')
            self.ret_list[1] = 1
            return

        parser = optparser.OptionsParser(options_dict)
        options_dict = parser.parse()
        Console.print(f'[{_FURGENT}]unset {option}[/]')
        self.ret_list[0] = options_dict
        self.ret_list[1] = 0