from config import colors, valid_modules
from rich import traceback, table, box, console

Console = console.Console()
traceback.install()

FALERT = colors.FALERT
FURGENT = colors.FURGENT
FSUCCESS = colors.FSUCCESS


class Options:
    """List values assigned to various options of the module"""

    def __init__(self, MODULE, option_dict: dict):
        self.module = MODULE
        self.option_dict = option_dict
        self.modules = valid_modules

    def showoriginal(self, option: str) -> str:
        value = self.option_dict[option]["value"]["value"]
        _type = self.option_dict[option]["value"]["type"]
        if type(value) is not (list or dict or tuple):
            return str(value)

        for rule in self.option_dict[option]["typerules"]:
            scheme: dict = self.option_dict[option]["typerules"][rule]
            delm = scheme.get("delimeter")
            if delm is not None and type(value) is list and _type == rule:
                return delm.join(value)
        else:
            return option

    def showOptions(self, trueval: bool = True):
        """
        Display values assigned to each options in a module.

        If no module is selected display values assigned to all options.
        """

        new_table = table.Table("Option", "Value", "Descrption", box=box.SIMPLE)

        if self.module in self.modules:
            COLOR: str = ""
            for option in self.modules[self.module]["options"]:
                display_value = (
                    self.option_dict[option]["value"]
                    if option in self.option_dict
                    else "[red]***N/A***[/]"
                )
                OptionIsRequired: bool = (
                    self.option_dict[option]["required"] is (not None and True)
                    if option in self.option_dict
                    else False
                )
                if option in self.option_dict:
                    if self.option_dict[option]["type"] == "dict":
                        display_value = (
                            self.showoriginal(option)
                            if not trueval
                            else self.option_dict[option]["value"]
                        )
                        if self.option_dict[option]["value"]["value"] in [None, ""]:
                            if OptionIsRequired:
                                COLOR = "red"
                            else:
                                COLOR = "yellow"
                        else:
                            COLOR = "white"
                    else:
                        if self.option_dict[option]["value"] in [None, ""]:
                            if OptionIsRequired:
                                COLOR = "red"
                            else:
                                COLOR = "yellow"
                        else:
                            COLOR = "white"
                else:
                    COLOR = "red"

                COLOR = COLOR if COLOR else "white"
                new_table.add_row(
                    f"[{COLOR}]{option}[/]",
                    f"[white]{display_value}",
                    self.option_dict[option]["description"]
                    if self.option_dict.get(option)
                    else "[red]***N/A***",
                )

        elif not self.module:
            for option in self.option_dict:
                display_value: str = str(
                    self.option_dict[option]["value"]
                    if option in self.option_dict
                    else f"[red]*N/A*[/]"
                )
                if self.option_dict[option]["type"] == "dict":
                    display_value = str(
                        self.showoriginal(option)
                        if not trueval
                        else self.option_dict[option]["value"]
                    )

                new_table.add_row(
                    option,
                    display_value,
                    self.option_dict[option].get("description"),
                )

        Console.print(new_table)
