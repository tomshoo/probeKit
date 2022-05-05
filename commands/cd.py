from os import path, chdir, getenv
from platform import platform
from config import colors
from rich import console
from modules.util.CommandUtils.ReturnStructure import RetObject
from modules.util.extra import args
Console = console.Console()

def run(arguments: list[str], ReturnObject: RetObject) -> RetObject:
    ArgumentMap: dict[str, str] = {}
    path_arg: str = ''
    for idx, argument in enumerate(arguments):
        ArgumentMap[argument.strip('-').lower()] = args(arguments, idx+1)
    if not ArgumentMap.get('path'):
        if 'Windows' in platform():
            home = getenv('USERPROFILE')
        else:
            home = getenv('HOME')
        if not home:
            Console.print(f'[{colors.FALERT}]Error: Could not find shift path...[/]')
            ReturnObject.exit_code = 1
        else:
            chdir(home)
    else:
        path_arg = ArgumentMap.get('path')
        path_arg = path.expanduser(path_arg)
        if path.exists(path_arg):
            try:
                chdir(path_arg)
                ReturnObject.exit_code = 0
            except PermissionError as err:
                Console.print(f'[{colors.FALERT}]Err: {err}[/]')
                ReturnObject.exit_code = 1
        else:
            Console.print(f'[{colors.FALERT}]Error: {path_arg} not found...[/]')
            ReturnObject.exit_code = 1
    return ReturnObject