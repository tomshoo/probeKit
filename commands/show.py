from modules.util.extra import get_args as _args
from modules.data.Help import Help
from rich.console import Console as con
from rich import table, box
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
        Console.print(f"[{_FALERT}]Err: No argument found[/]")
        ReturnObject.exit_code = 2
        return ReturnObject

    if "-h" in [x.lower() for x in arguments] or "--help" in [
        x.lower() for x in arguments
    ]:
        ReturnObject.exit_code = Help("show").showHelp()
        return ReturnObject

    sub_command: str = arguments[0].lower()
    arguments.pop(0)
    arguments_lower = [x.lower() for x in arguments]

    if sub_command == "options":
        trueval: bool = "-t" in arguments_lower or "--true-value" in arguments_lower
        if ("-m" in arguments_lower) ^ ("--module" in arguments_lower):
            flag = "-m" if "-m" in arguments_lower else "--module"
            module_name = _args(arguments_lower, arguments_lower.index(flag) + 1)
            if module_name:
                if module_name in valid_modules:
                    module = module_name
                else:
                    Console.print(
                        f"[{colors.FALERT}]Error: Invalid module {module_name}[/]"
                    )
                    ReturnObject.exit_code = 1
                    return ReturnObject
            else:
                Console.print(f"[{colors.FALERT}]Error: No module found to refer[/]")
                ReturnObject.exit_code = 1
                return ReturnObject
        elif ("-m" in arguments_lower) and ("--module" in arguments_lower):
            Console.print(
                f"[{colors.FALERT}]Alert: Please use either the short OR the long format, not both at single time.[/]"
            )
        options = Options.Options(module, ReturnObject.option_dict)
        options.showOptions(trueval=trueval)
        ReturnObject.exit_code = 0

    elif sub_command == "info":
        info = Info.Info(ReturnObject.module)
        ReturnObject.exit_code = info.showInfo()

    elif sub_command == "modules":
        print()
        print("Aviable modules are:")
        for data in valid_modules:
            if ReturnObject.module and ReturnObject.module == data:
                status = " (in use)"
            else:
                status = ""
            Console.print(f"\t[{_FSUCCESS}]{data}[/][{_FHIGHLIGHT}]{status}[/]")
        print()

        print('type "about [modulename]" to list details about a specific module\n')

        ReturnObject.exit_code = 0
    elif sub_command == "aliases":
        if "-e" in arguments_lower or "--expanded" in arguments_lower:
            new_table = table.Table("Name", "Command", "IsDefault", box=box.SIMPLE)
            for alias in ReturnObject.aliases:
                new_table.add_row(
                    f"[bold]{alias}[/]",
                    ReturnObject.aliases[alias][0],
                    "[green]*[/]" if ReturnObject.aliases[alias][1] else "",
                )
            Console.print(new_table)
            pass
        else:
            print("\nAvailable aliases are:")
            max_len = (
                max([len(x) for x in ReturnObject.aliases])
                if ReturnObject.aliases
                else 0
            )
            for alias in ReturnObject.aliases:
                if not ReturnObject.aliases[alias][1]:
                    Console.print(
                        f"{alias:{max_len}} -> [{_FHIGHLIGHT}]{ReturnObject.aliases[alias][0]}"
                    )
            print()
        ReturnObject.exit_code = 0

    elif sub_command == "macros":
        print("\nAvailable macros are:")
        max_len = (
            max([len(x) for x in ReturnObject.macros]) if ReturnObject.macros else 0
        )
        for macro in ReturnObject.macros:
            Console.print(
                f"{macro:{max_len}} ==> [{_FHIGHLIGHT}]{ReturnObject.macros[macro]}"
            )
        print()
        ReturnObject.exit_code = 0

    else:
        Console.print(
            f"[{_FALERT}]Error: Invalid argument\n"
            f"\trefer [{_FHIGHLIGHT}]help show[/] for more information.[/]\n"
        )
        ReturnObject.exit_code = 2

    return ReturnObject
