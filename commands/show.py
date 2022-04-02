from operator import le
from modules.util.extra import args as _args
from modules.data.Help import Help
from rich.console import Console as con
from config import colors, valid_modules
from modules.data import Info, Options
from modules.util.CommandUtils.ReturnStructure import RetObject

_FALERT = colors.FALERT
_FHIGHLIGHT = colors.FPROMPT
_FSUCCESS = colors.FSUCCESS

Console = con(highlight=False)
# def run(arguments: list=None, module: str=None, option_dict: str=None, aliases:dict[str] = None, macros:dict[str] = None) -> int:
def run(arguments: list[str], ReturnObject: RetObject) -> RetObject:
    module = ReturnObject.module
    if not _args(arguments, 0):
        Console.print(f'[{_FALERT}]Err: No argument found[/]')
        ReturnObject.exit_code = 2
        return ReturnObject

    if '-h' in [x.lower() for x in arguments] or '--help' in [x.lower() for x in arguments]:
        ReturnObject.exit_code = Help('show').showHelp()
        return ReturnObject
    elif '-t' in [x.lower() for x in arguments] or '--true' in [x.lower() for x in arguments]:
        trueval: bool = True
    else:
        trueval = False

    if len(arguments) > 1:
        if _args(arguments, 0) in ["info", "modules", "aliases", "macros"]:
            Console.print(f'[{_FALERT}]Error: {_args(arguments, 0)} did not expect any argument but found `{_args(arguments, 1)}`')
            ReturnObject.exit_code = 3
            return ReturnObject
        elif [y for y in arguments[1::] if y in [x.lower() for x in valid_modules]]:
            module = [y for y in arguments[1::] if y in [x.lower() for x in valid_modules]][0]
        else:
            if '-t' not in [x.lower() for x in arguments[1::]] or '--true' not in [x.lower() for x in arguments[1::]]:
                Console.print(f'[{_FALERT}]Error: invalid module found... refer `[{_FHIGHLIGHT}]show modules[/]` to get a list of available modules[/]')
                ReturnObject.exit_code = 1
                return ReturnObject

    if _args(arguments, 0).lower() == "options":
        options = Options.Options(module, ReturnObject.option_dict)
        options.showOptions(trueval=True) if trueval else options.showOptions(trueval=False)
        ReturnObject.exit_code = 0

    elif _args(arguments, 0).lower() == "info":
        info = Info.Info(ReturnObject.module)
        ReturnObject.exit_code = info.showInfo()

    elif _args(arguments, 0).lower() == "modules":
        print()
        print('Aviable modules are:')
        for data in valid_modules:
            if ReturnObject.module and ReturnObject.module == data:
                status = " (in use)"
            else:
                status = ""
            Console.print(f'\t[{_FSUCCESS}]{data}[/][{_FHIGHLIGHT}]{status}[/]')
        print()

        print('type "about [modulename]" to list details about a specific module\n')

        ReturnObject.exit_code = 0
    elif _args(arguments, 0).lower() == "aliases":
        print('\nAvailable aliases are:')
        max_len = max([len(x) for x in ReturnObject.aliases]) if ReturnObject.aliases else 0
        for alias in ReturnObject.aliases:
            Console.print(f'{alias:{max_len}} -> [{_FHIGHLIGHT}]{ReturnObject.aliases[alias]}')
        print()
        ReturnObject.exit_code = 0

    elif _args(arguments, 0).lower() == "macros":
        print('\nAvailable macros are:')
        max_len = max([len(x) for x in ReturnObject.macros]) if ReturnObject.macros else 0
        for macro in ReturnObject.macros:
            Console.print(f'{macro:{max_len}} ==> [{_FHIGHLIGHT}]{ReturnObject.macros[macro]}')
        print()
        ReturnObject.exit_code = 0

    else:
        Console.print(f'[{_FALERT}]Error: Invalid argument\n'
        f'\trefer [{_FHIGHLIGHT}]help show[/] for more information.[/]\n')
        ReturnObject.exit_code = 2

    return ReturnObject