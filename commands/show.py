from operator import le
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

    if '-h' in [x.lower() for x in arguments] or '--help' in [x.lower() for x in arguments]:
        return Help('show').showHelp()
    elif '-t' in [x.lower() for x in arguments] or '--true' in [x.lower() for x in arguments]:
        trueval: bool = True
    else:
        trueval = False

    if len(arguments) > 1:
        if _args(arguments, 0) in ["info", "modules", "aliases", "macros"]:
            Console.print(f'[{_FALERT}]Error: {_args(arguments, 0)} did not expect any argument but found `{_args(arguments, 1)}`')
            return 3
        elif _args(arguments, 1) in [x.lower() for x in valid_modules]:
            module = _args(arguments, 1)
        else:
            Console.print(f'[{_FALERT}]Error: invalid module found... refer `[{_FHIGHLIGHT}]show modules[/]` to get a list of available modules[/]')
            return 2

    if _args(arguments, 0).lower() == "options":
        options = Options.Options(module, option_dict)
        options.showOptions(trueval=True) if trueval else options.showOptions(trueval=False)
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