from modules.util.extra import args as _args
from modules.data.Help import Help
from rich.console import Console as con
from config import colors, valid_modules
from modules.data import Info, Options

_FALERT = colors.FALERT
_FHIGHLIGHT = colors.FPROMPT
_FSUCCESS = colors.FSUCCESS

Console = con(highlight=False)
def run(arguments: list=None, module: str=None, option_dict: str=None, aliases:dict[str] = None, macros:dict[str] = None) -> int:
    if not _args(arguments, 0):
        Console.print(f'[{_FALERT}]Err: No argument found[/]')
        return 2

    if _args(arguments, 1) and _args(arguments, 1) in valid_modules:
        module=_args(arguments, 1)
    else:
        Console.print(f'[{_FALERT}]Specified module was not invalid \'{_args(arguments, 1)}\'[/]')
        return 2

    if _args(arguments, 0).lower() in ['-h', '--help']:
        return Help('show').showHelp()
    
    if _args(arguments, 0).lower() == "options":
        options = Options.Options(module, option_dict)
        options.showOptions(trueval=True) if _args(arguments, 1) in ['-t', '--true'] else options.showOptions(trueval=False)
        return 0

    elif _args(arguments, 0).lower() == "info":
        info = Info.Info(module)
        return info.showInfo()

    elif _args(arguments, 0).lower() == "modules":
        print()
        print('Aviable modules are:')
        for data in valid_modules:
            if module and module == data:
                status = " (in use)"
            else:
                status = ""
            Console.print(f'\t[{_FSUCCESS}]{data}[/][{_FHIGHLIGHT}]{status}[/]')
        print()

        print('type "about [modulename]" to list details about a specific module\n')
        return 0
    elif _args(arguments, 0).lower() == "aliases":
        print('\nAvailable aliases are:')
        max_len = max([len(x) for x in aliases])
        for alias in aliases:
            Console.print(f'{alias:{max_len}} -> [{_FHIGHLIGHT}]{aliases[alias]}')
        print()
        return 0

    elif _args(arguments, 0).lower() == "macros":
        print('\nAvailable macros are:')
        max_len = max([len(x) for x in macros])
        for macro in macros:
            Console.print(f'{macro:{max_len}} ==> [{_FHIGHLIGHT}]{macros[macro]}')
        print()
        return 0

    else:
        Console.print(f'[{_FALERT}]Error: Invalid argument\n'
        f'\trefer [{_FHIGHLIGHT}]help show[/] for more information.[/]\n')
        return 3