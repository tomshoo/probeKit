from config import colors as _colors, valid_modules as _modules
from modules.data.Help import Help
from rich.console import Console
from modules.util.CommandUtils.ReturnStructure import RetObject

Console = Console(soft_wrap=True, highlight=False)

_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT

class use:
    def __init__(self, arguments: list[str], ReturnStruct: RetObject):
        self.ReturnStruct = ReturnStruct
        self.arguments = arguments

    def run(self) -> RetObject:
        args = [x.lower() for x in self.arguments]
        if not args:
            self.ReturnStruct.exit_code = 1
            Console.print(f'[{_FALERT}]Error: no module specified[/]')
            return self.ReturnStruct
        
        if '-h' in args or '--help' in args:
            self.ReturnStruct.exit_code = Help('use').showHelp()
            return self.ReturnStruct
        else:
            module = args

        if len(module) > 1:
            self.ReturnStruct.exit_code = 3
            Console.print(f'[{_FURGENT}]Alert: too many arguments[/]')
            return self.ReturnStruct

        else:
            if module[0] in _modules:
                if module[0] not in self.ReturnStruct.activated_module_list:
                    self.ReturnStruct.activated_module_list.append(module[0])
                else:
                    curridx: int = self.ReturnStruct.activated_module_list.index(module[0])
                    self.ReturnStruct.activated_module_list.append(self.ReturnStruct.activated_module_list.pop(curridx))
                self.ReturnStruct.exit_code = 0
                self.ReturnStruct.module = module[0]
                Console.print(f'[{_FURGENT}]MODULE => {module[0]}[/]')

            else:
                self.ReturnStruct.exit_code = 1
                Console.print(f'[{_FALERT}]Error: Invalid module \'{module[0]}\'[/]')
                Console.print(f'[{_FURGENT}]*Hint: Refer to command `show modules` for a list of available modules[/]')
                return self.ReturnStruct

        return self.ReturnStruct