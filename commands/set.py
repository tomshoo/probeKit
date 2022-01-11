from config import colors as _colors, OPTIONS
from modules.util.extra import trim as _trim, args as _args
from modules.util import optparser
from rich import console,traceback
from typing import List, Union
traceback.install()
Console = console.Console()

_FALERT = _colors.FALERT
_FSUCCESS = _colors.FSUCCESS

class set_class:
    def __init__(self, option_dict: dict, options: list):
        self.ret_list = [option_dict, 0]
        self.options = options

    def run(self) -> List[Union[dict, int]]:
        options: str = ' '.join(self.options)

        if options.lower() == "all":
            Console.print(f'[{_FSUCCESS}]set all[/]')
            option_dict: dict = self.ret_list[0]
            for option in OPTIONS:
                if option_dict[option]['type'] == "dict": option_dict[option]['value']['value'] = OPTIONS[option]
                else: option_dict[option]['value'] = OPTIONS[option]

            parser = optparser.OptionsParser(option_dict)
            option_dict = parser.parse()
            self.ret_list[0] = option_dict
        elif ' ' in options:
            assignment = options.split(' ')
            for data in assignment:
                option = _args(data.split('='), 0).lower()
                value = _args(data.split('='), 1)
                self.assign(option, value)

        else:
            options = options.split('=')
            option = _args(options, 0).lower()
            value = _args(options, 1)
            self.assign(_trim(option), _trim(value))

        return self.ret_list

    def assign(self, option: str, value: str):
        options = self.ret_list[0]
        if options.get(option):
            if options[option]['type'] != "dict": options[option]['value'] = value
            else: options[option]['value']['value'] = value
        else:
            Console.print(f'[{_FALERT}]Error: Invalid option \'{option}\'[/]')
            self.ret_list[1] = 1
            return
        
        parser = optparser.OptionsParser(options)
        options = parser.parse()
        print(option, '=>', value)
        self.ret_list[0] = options
        self.ret_list[1] = 0