from modules.util.utils import args as _args
from rich.console import Console as con
from config import colors, valid_modules
from modules.data.OptInfHelp import Info, Options

_FALERT = colors.FALERT
_FHIGHLIGHT = colors.FPROMPT
_FSUCCESS = colors.FSUCCESS

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
        print()
        print('Aviable modules are:')
        for data in valid_modules:
            Console.print(f'\t[{_FSUCCESS}]{data}[/]')
        print()

        if module:
            Console.print(f'Current selected module: [{_FSUCCESS}]{module}[/]')
            print('type "about" to list more details about the selected module\n')

        print('type "about [modulename]" to list details about a specific module\n')
        return 0

    else:
        Console.print(f'[{_FALERT}]Error: Invalid argument\n'
        f'\trefer [{_FHIGHLIGHT}]help show[/] for more information.[/]\n')
        return 3