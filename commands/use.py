from config import colors as _colors, valid_modules as _modules
from modules.data.Help import Help
from rich.console import Console
from typing import List, Union

Console = Console(soft_wrap=True, highlight=False)

_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class use:
    def __init__(self, module: list[str] = None, modlist: list[str] = None):
        self.ret_list = [modlist, 0]
        self.module = module

    def run(self) -> List[Union[str, int]]:
        args = [x.lower() for x in self.module]
        if not args:
            self.ret_list[1] = 1
            Console.print(f'[{_FALERT}]Error: no module specified[/]')
        
        if '-h' in args or '--help' in args:
            return ['', Help('use').showHelp()]
        else:
            module = args

        if len(module) > 1:
            self.ret_list[1] = 1
            Console.print(f'[{_FURGENT}]Alert: too many arguments[/]')

        else:
            if module[0] in _modules:
                if module[0] not in self.ret_list[0]: self.ret_list[0].append(module[0])
                else:
                    curridx: int = self.ret_list[0].index(module[0])
                    self.ret_list[0].append(self.ret_list[0].pop(curridx))
                self.ret_list[1] = 0
                Console.print(f'[{_FURGENT}]MODULE => {module[0]}[/]')

            else:
                self.ret_list[1] = 1
                Console.print(f'[{_FALERT}]Error: Invalid module \'{module[0]}\'[/]')
                Console.print(f'[{_FURGENT}]*Hint: Refer to command `show modules` for a list of available modules[/]')

        return self.ret_list