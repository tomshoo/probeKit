from config import colors as _colors, valid_modules as _modules
from rich.console import Console
from typing import List, Union


_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class use:
    def __init__(self, module: list = None, modlist: list = None):
        self.ret_list = [modlist, 0]
        self.module = module

    def run(self) -> List[Union[str, int]]:
        modlist: list = self.ret_list[0]
        module = self.module
        if not module:
            self.ret_list[1] = 1
            Console().print(f'[{_FALERT}]Error: no module specified[/]')

        elif len(module) > 1:
            self.ret_list[1] = 1
            Console().print(f'[{_FURGENT}]Alert: too many arguments[/]')

        else:
            if module[0] in _modules:
                if module[0] not in self.ret_list[0]: self.ret_list[0].append(module[0])
                else:
                    curridx: int = self.ret_list[0].index(module[0])
                    self.ret_list[0].append(self.ret_list[0].pop(curridx))
                self.ret_list[1] = 0
                Console().print(f'[{_FURGENT}]MODULE => {module[0]}[/]')

            else:
                self.ret_list[1] = 1
                Console().print(f'[{_FALERT}]Error: Invalid module[/]')

        return self.ret_list