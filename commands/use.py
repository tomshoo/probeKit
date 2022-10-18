from config import colors as _colors
from config import valid_modules as _modules
from modules.data.Help import Help
from modules.util.CommandUtils.ReturnStructure import RetObject
from rich.console import Console

from . import Runnable

console = Console(soft_wrap=True, highlight=False)

_FALERT = _colors.FALERT
_FURGENT = _colors.FURGENT


class UseModule(Runnable):
    def run(self) -> RetObject:
        args = [x.lower() for x in self.args]
        if not args:
            self.retobj.exit_code = 1
            console.print(f"[{_FALERT}]Error: no module specified[/]")
            return self.retobj

        if "-h" in args or "--help" in args:
            self.retobj.exit_code = Help("use").showHelp()
            return self.retobj
        else:
            module = args

        if len(module) > 1:
            self.retobj.exit_code = 3
            console.print(f"[{_FURGENT}]Alert: too many arguments[/]")
            return self.retobj

        else:
            if module[0] in _modules:
                if module[0] not in self.retobj.activated_module_list:
                    self.retobj.activated_module_list.append(module[0])
                else:
                    curridx: int = self.retobj.activated_module_list.index(
                        module[0]
                    )
                    self.retobj.activated_module_list.append(
                        self.retobj.activated_module_list.pop(curridx)
                    )
                self.retobj.exit_code = 0
                self.retobj.module = module[0]
                console.print(f"[{_FURGENT}]MODULE => {module[0]}[/]")

            else:
                self.retobj.exit_code = 1
                console.print(
                    f"[{_FALERT}]Error: Invalid module '{module[0]}'[/]")
                console.print(
                    f"[{_FURGENT}]*Hint: Refer to command `show modules` for a list of available modules[/]"
                )
                return self.retobj

        return self.retobj
