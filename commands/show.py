from modules.util.utils import args as _args
from rich.console import Console as con
from config import colors
from modules.data.OptInfHelp import Info, Options
from modules.data.AboutList import moduleHelp

_FALERT = colors.FALERT
_FHIGHLIGHT = colors.FPROMPT

Console = con()
def run(arguments: list=None, module: str=None, option_dict: str=None) -> int:
    if not _args(arguments, 0):
        Console.print(f'[{_FALERT}]Err: No argument found[/]')
        return 2
    
    if _args(arguments, 0).lower() == "options":
        options = Options(module, option_dict)
        options.showOptions(trueval=True) if _args(arguments, 1) in ['-t', '--true'] else options.showOptions(trueval=False)
        return 0

    elif _args(arguments, 0).lower() == "info":
        info = Info(module)
        return info.showInfo()

    elif _args(arguments, 0).lower() == "modules":
        try:
            moduleHelp(module).listmodules()
            return 0
        except Exception as e:
            Console.print(f'[{_FALERT}]{str(e)}[/]')
            return 1

    else:
        Console.print(f'[{_FALERT}]Error: Invalid argument\n'
        f'\trefer [{_FHIGHLIGHT}]help show[/] for more information.[/]\n')
        return 3