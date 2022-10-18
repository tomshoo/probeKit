from platform import platform
from os import system, path
from modules.util.extra import get_args
from modules.util.CommandUtils.ReturnStructure import RetObject
import readline
from sys import exit

from . import Runnable


class ClearScreen(Runnable):
    def run(self) -> RetObject:
        if get_args(self.args, 0) and get_args(self.args, 0) in ["-h", "--history"]:
            readline.clear_history()

            if self.retobj.histfile:
                if path.exists(self.retobj.histfile):
                    with open(self.retobj.histfile, "w") as hist_cls:
                        hist_cls.write("#Clear\n")

        if "Windows" in platform():
            system("cls")

        else:
            print(chr(27) + "2[j")
            print("\033c")
            print("\x1bc")

        if get_args(self.args, 0) and get_args(self.args, 0) == "-e":
            exit(self.retobj.exit_code)

        self.retobj.exit_code = 0
        return self.retobj
