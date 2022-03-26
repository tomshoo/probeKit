from modules.util.ReturnStructure import RetObject
from rich.console import Console
from config import colors
Console = Console(soft_wrap=True, highlight=False)

def run(_arguments: list[str], ReturnObject: RetObject) -> RetObject:
    if not ReturnObject.module:
        Console.print(f'[{colors.FURGENT}]Alert: No module selected.. nothing to back from[/]')
        ReturnObject.exit_code = 1
    else:
        if ReturnObject.module == (ReturnObject.activated_module_list[-1] if ReturnObject.activated_module_list else None):
            try:
                ReturnObject.activated_module_list.pop()
            except IndexError as e:
                print(e)
        else:
            pass

        ReturnObject.module = ReturnObject.activated_module_list.pop() if ReturnObject.activated_module_list else ''
    return ReturnObject