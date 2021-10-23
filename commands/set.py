from config import colors as _colors, variables as _variables
from modules.util.utils import trim as _trim, args as _args, optionparser as _optparser

_FALERT = _colors.FALERT

class set_class:
    def __init__(self, option_dict: dict, options: list):
        self.ret_list = [option_dict, 0]
        self.options = options

    def run(self) -> list:
        options: str = ' '.join(self.options)

        if ' ' in options:
            assignment = options.split(' ')
            for data in assignment:
                option = _args(data.split('='), 0)
                value = _args(data.split('='), 1)
                self.assign(option, value)

        else:
            options = options.split('=')
            option = _args(options, 0)
            value = _args(options, 1)
            self.assign(_trim(option), _trim(value))

        return self.ret_list

    def assign(self, option: str, value: str):
        options = self.ret_list[0]
        if options.get(option):
            if options[option]['type'] != "dict":
                options[option]['value'] = value
            else:
                options[option]['value']['value'] = value
        else:
            print(f'{_FALERT}Error: Invalid option \'{option}\'')
            self.ret_list[1] = 1
            return
        
        options = _optparser(options)
        print(option, '=>', options[option]['value'])
        self.ret_list[0] = options
        self.ret_list[1] = 0