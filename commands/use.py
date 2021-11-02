from config import colors as _colors, valid_modules as _modules
from rich.console import Console


_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class use:
    def __init__(self, module: list = None):
        self.ret_list = [module, 0]

    def run(self) -> list:
        module = self.ret_list[0]
        if not module:
            self.ret_list[0] = ''
            self.ret_list[1] = 1
            Console().print(f'[{_FALERT}]Error: no module specified[/]')

        elif len(module) > 1:
            self.ret_list[0] = ''
            self.ret_list[1] = 1
            Console().print(f'[{_FURGENT}]Alert: too many arguments[/]')

        else:
            if module[0] in _modules:
                self.ret_list[0] = module[0]
                self.ret_list[1] = 0
                Console().print(f'[{_FURGENT}]MODULE => {module[0]}[/]')

            else:
                self.ret_list[0] = ''
                self.ret_list[1] = 1
                Console().print(f'[{_FALERT}]Error: Invalid module[/]')

        return self.ret_list