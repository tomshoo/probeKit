from os import path, chdir, getenv
from platform import platform
from config import colors
from rich import console
from modules.util.CommandUtils.ReturnStructure import RetObject
from modules.util.extra import get_args

from . import Runnable

Console = console.Console()


class ChangeDir(Runnable):
    def run(self) -> RetObject:
        ArgumentMap: dict[str, str] = {}
        path_arg: str = ""
        for idx, argument in enumerate(self.args):
            ArgumentMap[argument.strip("-").lower()] = self.args[idx + 1]
        if not ArgumentMap.get("path"):
            if "Windows" in platform():
                home = getenv("USERPROFILE")
            else:
                home = getenv("HOME")
            if not home:
                Console.print(
                    f"[{colors.FALERT}]Error: Could not find shift path...[/]")
                self.retobj.exit_code = 1
            else:
                chdir(home)
        else:
            path_arg = ArgumentMap.get("path", "")
            path_arg = path.expanduser(path_arg)
            if path.exists(path_arg):
                try:
                    chdir(path_arg)
                    self.retobj.exit_code = 0
                except PermissionError as err:
                    Console.print(f"[{colors.FALERT}]Err: {err}[/]")
                    self.retobj.exit_code = 1
            else:
                Console.print(
                    f"[{colors.FALERT}]Error: {path_arg} not found...[/]")
                self.retobj.exit_code = 1
        return self.retobj
