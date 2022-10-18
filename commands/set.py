from config import colors as _colors, OPTIONS
from modules.util.extra import trim
from modules.util import optparser
from modules.util.splitters import splitter
from modules.data.Help import Help
from modules.util.CommandUtils.ReturnStructure import RetObject
from rich import console as _console, traceback
from fuzzywuzzy import process

traceback.install()
console = _console.Console()

_FALERT = _colors.FALERT
_FSTYLE = _colors.FPROMPT
_FURGENT = _colors.FURGENT


class Set:
    def __init__(self, arguments, return_obj: RetObject) -> None:
        self.args = arguments
        self.retobj = return_obj

    def run(self) -> RetObject:
        if not self.args:
            self.retobj.exit_code = 1
            return self.retobj

        if "-h" in (l := [a.lower() for a in self.args]) or "--help" in l:
            self.retobj.exit_code = Help("set").showHelp()
            return self.retobj

        kvpairs = [[x.strip() for x in l1 if x]
                   for l1 in splitter(' '.join(self.args[1::]), inner_delm='=', outer_delm=',')]

        if (func := {
            "option": self.assign_options,
            "alias": self.assign_alias,
            "macro": (lambda k, v: self.retobj.macros.update({k: v}))
        }.get(self.args[0].lower())) is not None:
            if not kvpairs and func == self.assign_options:
                for pair in OPTIONS.items():
                    func(*pair)
                self.retobj.exit_code = 0
                return self.retobj

            elif not kvpairs:
                console.print(
                    f"[{_FALERT}]Error: Key value pair is required for [{_FSTYLE}]'{func.__name__}'[/][/]")
                self.retobj.exit_code = 1
                return self.retobj

            for kvpair in kvpairs:
                if len(kvpair) != 2:
                    console.print(
                        f'[{_FALERT}]Error: Invalid kvset for item [{_FSTYLE}]{kvpair}[/][/]')
                    self.retobj.exit_code = 1
                    return self.retobj

                func(*kvpair)
        else:
            value = process.extractOne(
                self.args[0], ["option", "alias", "macro"])
            if value is not None and value[1] > 50:
                console.print(
                    f"[{_FALERT}]Error unrecognized action: '{self.args[0]}'..." +
                    f" Did you mean [{_FURGENT}]'{value[0]}'[/]?[/]")
            else:
                console.print(
                    f"[{_FALERT}]Error: unrecognized action '{self.args[0]}'[/]")
            pass

        return self.retobj

    def assign_options(self, option: str, value: str):
        options = self.retobj.option_dict
        if options.get(option):
            if options[option]["type"] != "dict":
                options[option]["value"] = value
            else:
                options[option]["value"]["value"] = value
        else:
            console.print(f"[{_FALERT}]Error: Invalid option '{option}'[/]")
            self.retobj.exit_code = 1
            return

        parser = optparser.OptionsParser(options)
        options = parser.parse()
        if not options[1]:
            self.retobj.exit_code = 1
            return
        print(option, "=>", value)
        self.retobj.option_dict = options[0]
        self.retobj.exit_code = 0

    def assign_alias(self, alias: str, command: str) -> None:
        aliases = self.retobj.aliases
        exit_code = self.retobj.exit_code

        if not alias.isalnum():
            console.print(
                "[red]Alert: Alias name can only contain alphabets and numbers[/]"
            )
            self.retobj.exit_code = 1
            return

        alias = trim(alias)
        command = trim(command)
        command = command.strip('"')
        command = command.strip("'")
        is_alias: bool = bool(aliases.get(command.split()[0]))
        while is_alias:
            token = command.split()[0]
            token_alias = aliases.get(token)
            if token_alias:
                if token_alias[0] == token:
                    is_alias = False
                    break
                command = command.replace(
                    token, aliases.get(token, [token])[0], 1)
            else:
                is_alias = False
        print(alias, ":", command)
        aliases[alias] = [command, False]

        self.retobj.aliases = aliases
        self.retobj.exit_code = exit_code
