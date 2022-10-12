#!/usr/bin/env python3

# Imports
from modules.util.led import start_editor
from config import valid_modules as _modules
from config import MODULE, aliases, colors, macros, option_dict
from commands import banner
import modules.data.AboutList as aboutList
import argparse
import os
import platform
import re
import readline
import subprocess
import sys

from fuzzywuzzy import process
from rich import console, traceback

from modules.util import extra
from modules.util import hist as history
from modules.util import optparser, splitters
from modules.util.CommandUtils.CommandStruct import CreateCommand

traceback.install()
Console = console.Console(soft_wrap=True, highlight=False)


class SudoError(Exception):
    pass


# Setup Utils
optionparser = optparser.OptionsParser(option_dict)
option_dict = optionparser.parse()
ExitException = extra.ExitException
completer = extra.completer(extra.completers.interpreter)

# Setting up colors (edit these in UserConfig.py)
FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FURGENT = colors.FURGENT
FSTYLE = colors.FPROMPT

# Display time during statup
if not (
    "-h" in sys.argv or "--help" in sys.argv or "-l" in sys.argv or "--list" in sys.argv
):
    print(f"current session started at {extra.timefunc.datevalue()}")

if extra.get_args(sys.argv, 1) in ["-h", "--help"]:
    banner.paint()
    print()

parser = argparse.ArgumentParser(
    description="Command line toolkit for basic reconnaisance"
)
parser.add_argument(
    "-c", "--command", help="custom command to run from outside the session"
)
parser.add_argument(
    "-m",
    "--module",
    help="Start with a specified module (Overrides default module set in config)",
)
parser.add_argument(
    "-q", "--quiet", help="Do not display banner on startup", action="store_true"
)
parser.add_argument(
    "-l", "--list", help="list available modules", action="store_true")

args = parser.parse_args()

if args.list:
    Console.print(f"[{FSUCCESS}]Available module are:")
    for module in _modules:
        Console.print(f"\t-> [{FURGENT}]{module}[/]")
    print()
    sys.exit(0)

if not args.quiet:
    banner.paint()

if args.module and args.module not in _modules:
    Console.print(
        f"[{FALERT}]Alert: Invalid module `{args.module}`, defaulting to no module[/]"
    )

# Checks if history file already exists or not
if "Windows" not in platform.platform():
    histfile: str | None = os.path.join(
        os.path.expanduser("~"), ".probeKit.history")
    if os.path.exists(histfile):
        readline.read_history_file(histfile)
else:
    histfile = None

if not extra.isAdmin():
    Console.print(
        f"[{FURGENT}]Warning: `osprobe` and `UDP Scanning` may not work as expected..."
    )


# Session starts over here
# Not the best way to do it but it works so...
class input_parser:
    def __init__(self):
        self.exit_code: int = 0
        # Variables also known as options to the user
        self.option_dict: dict = option_dict

        self.module: str = (
            MODULE if not args.module or args.module not in _modules else args.module
        )
        self.modlist: list = []
        self.aliases: dict = aliases
        self.macros: dict = macros

    def parser(self, value: str):
        value = value.split('#', 1)[0]

        if not value:
            return

        macrolist: list[str] = re.findall("\\$\\(.*?\\)", value)
        mlen = len(macrolist)
        macrolist[mlen:mlen] = re.findall("(?<!\\w)\\$\\w+", value)

        for ident in macrolist:
            macroname = ident.lstrip("$").lstrip("(").rstrip(")")

            value = value.replace(ident, macros.get(
                macroname, macroname if ident.endswith(")") else ""))

        allcmds = splitters.splitter(value, outer_delm=';')
        for toklist in allcmds:
            toklist[0] = aliases.get(toklist[0], (toklist[0], False))[0]
            self.executor([tok for tok in toklist if tok])

    def executor(self, toklist: list[str]):
        verb: str = toklist[0].lower()

        CommandStruct = CreateCommand(
            arguments=toklist[1::],
            option_dict=self.option_dict,
            aliases=self.aliases,
            macros=self.macros,
            activated_module_list=self.modlist,
            module=self.module,
            histfile=histfile,
        ).run(verb)

        if CommandStruct is not None and CommandStruct.command_found:
            self.option_dict = CommandStruct.option_dict
            self.aliases = CommandStruct.aliases
            self.macros = CommandStruct.macros
            self.modlist = CommandStruct.activated_module_list
            self.module = CommandStruct.module
            self.exit_code = CommandStruct.exit_code

        elif verb == "do":
            try:
                times: int = 1
                if "-t" in toklist:
                    times = int(t) if (t := extra.get_args(
                        toklist, toklist.index("-n") + 1)) is not None else 1
                noreturn: bool = True if "-n" in toklist else False
                self.do(toklist[1], times, noreturn)
            except ValueError:
                Console.print(f"[{FALERT}]Error: Invalid argument[/]")

        elif verb == "led":
            init_editor = start_editor(toklist)
            init_editor.start_led()

        # Create an exception which exits the try block and then exits the session
        elif verb == "exit":
            if extra.get_args(toklist, 1) == "-q":
                raise ExitException()
            else:
                raise ExitException(f"probeKit: exiting session")

        elif verb == "about":
            if extra.get_args(toklist, 1):
                mod = extra.get_args(toklist, 1)
                aboutList.moduleHelp(mod).aboutModule(mod)
            else:
                aboutList.moduleHelp(self.module).aboutModule(self.module)

        else:
            env_path: str | None = os.getenv("PATH")
            if env_path is not None:
                PATH: list = (env_path + ":").split(":")
            else:
                PATH = []
            for path in PATH:
                try:
                    with open(
                        path + "/" + verb, "r"
                    ) if "Windows" not in platform.platform() else open(
                        path + "\\" + verb
                    ) as cmd:
                        content = cmd.read().lower()
                except UnicodeDecodeError:
                    pass
                except FileNotFoundError:
                    pass
                else:
                    if len(re.findall("(g)?sudo*", content)) > 0:
                        Console.print(
                            f"[{FALERT}]Warning: sudo or gsudo found in script, not running..."
                        )
                        raise SudoError()
            if verb.lower() in ["sudo", "gsudo"]:
                Console.print(
                    f"[{FALERT}]Warning: using sudo or gsudo is prohibited for security reasons[/]"
                )
                raise SudoError()
            try:
                if not extra.isAdmin():
                    if "Windows" not in platform.platform():
                        self.exit_code = subprocess.call((toklist))
                    else:
                        self.exit_code = subprocess.run(
                            ' '.join(toklist)).returncode

                else:
                    Console.print(
                        f"[{FALERT}]Error: Invalid command '{verb}'[/]")
                    self.exit_code = 1

            except FileNotFoundError:
                Console.print(f"[{FALERT}]Error: Invalid command '{verb}'[/]")
                fuzzy_match_list: list[str] = [
                    x[0]
                    for x in process.extractBests(verb, extra.completers.interpreter)
                ]
                Console.print(f"[{colors.FURGENT}]Perhaps you meant: [/]")
                for match in fuzzy_match_list:
                    Console.print(f"\t[{colors.FPROMPT}]{match}[/]")
                self.exit_code = 1

    def prompt(self, check: int = 0) -> int:
        if self.exit_code == 0:
            COLOR: str = colors.FSUCCESS
        elif self.exit_code == 130:
            COLOR: str = colors.FURGENT
        else:
            COLOR: str = colors.FALERT

        if not self.module:
            prompt_str: str = f"\\[probkit]: [{COLOR}]{self.exit_code}[/]$> "
        else:
            prompt_str: str = f"\\[probeKit]: [{FSTYLE}]({self.module})[/]: [{COLOR}]{self.exit_code}[/]$> "
        if check == 0:
            value = console.Console(soft_wrap=True).input(prompt_str)
        else:
            external_command: str = args.command
            splitted: list = external_command.split(" ")
            splitted.append(";exit -q")
            value = " ".join(splitted)
            check = 0

        if value:
            value = extra.trim(value)
            if value[-1] == "\\":
                concatinator: list = [value[:-1]]
                while True:
                    line: str = input("..> ")
                    if not line:
                        break
                    concatinator.append(line)
                value = "".join(concatinator)
            self.parser(value)
            if "Windows" not in platform.platform():
                hist = history.register_history(value)
                hist.write_history()
        return 0

    def main(self):
        check: int = 1 if args.command else 0

        readline.set_completer(completer.completion)
        readline.parse_and_bind("tab: complete")

        # Initial module is set to blank
        # Set it to any other module if you want a default module at startup

        if self.module in _modules or self.module == "":
            pass

        else:
            Console.print(
                f"[{FALERT}][-] No such module: [bold underline]'{self.module}'[/][/]"
            )
            sys.exit(1)

        try:
            while True:
                check = self.prompt(check)

        except EOFError:
            print()
            pass

        except KeyboardInterrupt:
            self.exit_code = 130
            print("\n")
            self.main()

        except SudoError:
            self.exit_code = 1
            self.main()

        except ExitException as e:
            Console.print(f"[{FALERT}]" + e.__str__() + "[/]")
            extra.ExitSession(
                self.exit_code
            ) if "Windows" in platform.platform() else extra.ExitSession(
                self.exit_code, histfile
            )

    def do(self, command: str, times: int = 1, noreturn: bool = False) -> None:
        command = command.replace("_", " ")
        if noreturn:
            try:
                for _ in range(times):
                    self.parser(command)
            except Exception as e:
                print(e)
            self.exit_code = 0
        else:
            for _ in range(times):
                self.parser(command)
        pass


if __name__ == "__main__":
    new_parser = input_parser()
    new_parser.main()
