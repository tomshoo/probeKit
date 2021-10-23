from config import colors as _colors
from modules.util.utils import optionparser

_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class unset_val:
    def __init__(self, option_dict: dict, options: list):
        ret_list = [option_dict, 0]
        self.ret_list = ret_list
        self.options = options

    def run(self) -> list:
        for option in self.options:
            self.unassign(option)
        return self.ret_list

    def unassign(self, option: str):
        options_dict: dict = self.ret_list[0]
        if options_dict.get(option):
            if options_dict[option]['type'] != "dict":
                options_dict[option]['value'] = ""
            else:
                options_dict[option]['value']['value'] = ""
                options_dict[option]['value']['type'] = ""
        else:
            print(f'{_FALERT}Error: invalid option \'{option}\'')
            self.ret_list[1] = 1
            return

        options_dict = optionparser(options_dict)
        print(f'{_FURGENT}unset {option}')
        self.ret_list[0] = options_dict
        self.ret_list[1] = 0