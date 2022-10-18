from modules.util.extra import get_args as _args
from modules.data.Help import Help
from rich.console import Console as con
from rich import table, box
from config import colors, valid_modules
from modules.data import Info, Options
from modules.util.CommandUtils.ReturnStructure import RetObject

from . import Runnable

_FALERT = colors.FALERT
_FHIGHLIGHT = colors.FPROMPT
_FSUCCESS = colors.FSUCCESS

Console = con(highlight=False)


class ShowVars(Runnable):
    def run(self) -> RetObject:
        module = self.retobj.module
        if not _args(self.args, 0):
            Console.print(f"[{_FALERT}]Err: No argument found[/]")
            self.retobj.exit_code = 2
            return self.retobj

        if "-h" in [x.lower() for x in self.args] or "--help" in [
            x.lower() for x in self.args
        ]:
            self.retobj.exit_code = Help("show").showHelp()
            return self.retobj

        sub_command: str = self.args[0].lower()
        self.args.pop(0)
        arguments_lower = [x.lower() for x in self.args]

        if sub_command == "options":
            trueval: bool = "-t" in arguments_lower or "--true-value" in arguments_lower
            if ("-m" in arguments_lower) ^ ("--module" in arguments_lower):
                flag = "-m" if "-m" in arguments_lower else "--module"
                module_name = _args(
                    arguments_lower, arguments_lower.index(flag) + 1)
                if module_name:
                    if module_name in valid_modules:
                        module = module_name
                    else:
                        Console.print(
                            f"[{colors.FALERT}]Error: Invalid module {module_name}[/]"
                        )
                        self.retobj.exit_code = 1
                        return self.retobj
                else:
                    Console.print(
                        f"[{colors.FALERT}]Error: No module found to refer[/]")
                    self.retobj.exit_code = 1
                    return self.retobj
            elif ("-m" in arguments_lower) and ("--module" in arguments_lower):
                Console.print(
                    f"[{colors.FALERT}]Alert: Please use either the short OR the long format, not both at single time.[/]"
                )
            options = Options.Options(module, self.retobj.option_dict)
            options.showOptions(trueval=trueval)
            self.retobj.exit_code = 0

        elif sub_command == "info":
            info = Info.Info(self.retobj.module)
            self.retobj.exit_code = info.showInfo()

        elif sub_command == "modules":
            print()
            print("Aviable modules are:")
            for data in valid_modules:
                if self.retobj.module and self.retobj.module == data:
                    status = " (in use)"
                else:
                    status = ""
                Console.print(
                    f"\t[{_FSUCCESS}]{data}[/][{_FHIGHLIGHT}]{status}[/]")
            print()

            print(
                'type "about [modulename]" to list details about a specific module\n')

            self.retobj.exit_code = 0
        elif sub_command == "aliases":
            if "-e" in arguments_lower or "--expanded" in arguments_lower:
                new_table = table.Table(
                    "Name", "Command", "IsDefault", box=box.SIMPLE)
                for alias in self.retobj.aliases:
                    new_table.add_row(
                        f"[bold]{alias}[/]",
                        self.retobj.aliases[alias][0],
                        "[green]*[/]" if self.retobj.aliases[alias][1] else "",
                    )
                Console.print(new_table)
                pass
            else:
                print("\nAvailable aliases are:")
                max_len = (
                    max([len(x) for x in self.retobj.aliases])
                    if self.retobj.aliases
                    else 0
                )
                for alias in self.retobj.aliases:
                    if not self.retobj.aliases[alias][1]:
                        Console.print(
                            f"{alias:{max_len}} -> [{_FHIGHLIGHT}]{self.retobj.aliases[alias][0]}"
                        )
                print()
            self.retobj.exit_code = 0

        elif sub_command == "macros":
            print("\nAvailable macros are:")
            max_len = (
                max([len(x) for x in self.retobj.macros]
                    ) if self.retobj.macros else 0
            )
            for macro in self.retobj.macros:
                Console.print(
                    f"{macro:{max_len}} ==> [{_FHIGHLIGHT}]{self.retobj.macros[macro]}"
                )
            print()
            self.retobj.exit_code = 0

        else:
            Console.print(
                f"[{_FALERT}]Error: Invalid argument\n"
                f"\trefer [{_FHIGHLIGHT}]help show[/] for more information.[/]\n"
            )
            self.retobj.exit_code = 2

        return self.retobj
