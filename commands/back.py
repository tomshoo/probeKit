from modules.util.CommandUtils.ReturnStructure import RetObject
from rich.console import Console
from config import colors

from . import Runnable

console = Console(soft_wrap=True, highlight=False)


class MoveBack(Runnable):
    def run(self) -> RetObject:
        if not self.retobj.module:
            console.print(
                f'[{colors.FURGENT}]Alert: No module selected.. nothing to back from[/]')
            self.retobj.exit_code = 1
        else:
            if self.retobj.module == (self.retobj.activated_module_list[-1] if self.retobj.activated_module_list else None):
                try:
                    self.retobj.activated_module_list.pop()
                except IndexError as e:
                    print(e)
            else:
                pass

            self.retobj.module = self.retobj.activated_module_list.pop(
            ) if self.retobj.activated_module_list else ''
        return self.retobj
