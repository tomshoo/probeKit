# This is the data-information module which will print help for the interpreter and information about selected module

from config import colors, valid_modules
from platform import platform
from rich import traceback, table, box, console
Console = console.Console()
traceback.install()

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FURGENT = colors.FURGENT

class PromptHelp():
    """This class prints help for the interpreter."""
    def __init__(self, command : str):
        self.command = command

    def showHelp(self):
        """Show the actual help."""
        command = self.command

        # Checks whether the shell is module interpreter or module selector session
        if command == '':
            Console.print(f'\n[{FSUCCESS}]Usage: [verb] [options]\n'+
            'Available verbs are:\n\n'+
            '\t use\t\t (*)use an available module\n'+
            '\t show\t\t (*)shows information on provided argument\n'+
            '\t set\t\t (*)assignes values to available options\n'+
            '\t unset\t\t (*)unassigns value from the provided option\n'+
            '\t help\t\t prints this help message\n'+
            '\t exit\t\t exits the whole interpreter\n'+
            '\t back\t\t moves back to the module selector\n'+
            '\t clear\t\t clears screen\n'+
            '\t run\t\t runs the selected module\n'+
            '\t about\t\t (*)prints details about specified module\n'+
            '\t banner\t\t prints an ascii banner\n'+
            '\t alias\t\t (*)set an alias for a command\n'+
            '\t unalias\t (*)unset a pre-existing alias\n'+
            '\nRun help \[command] for more information:\n'+
            '\t -> only the commands marked with (*) have a seperate help[/]\n'
            )
            return 0

        elif command == 'show':
            Console.print(f'[{FSUCCESS}]\n show:\t Shows information on provided argument\n'
            '\t Usage: show [argument]\n'
            '\t Available arguments are:\n'
            '\t\t | options: shows values assigned to the options available for the selected module\n'
            '\t\t\t - shows all assigned values if no module is selected\n\n'
            '\t\t | info: shows available options for selected module\n'
            '\t\t | status: prints exit status of previous command[/]\n'
            '\t\t | modules: list all available modules\n')
            return 0

        elif command == 'set':
            Console.print(f'[{FSUCCESS}]\n set:\t Sets the provided value to the provided option\n'
            '\t Usage: set \[option1]=\[value1] \[option2]=\[value2] ...\n'
            '\t Example: > set thost=127.0.0.1 tport=443,5432,8000 proto=tcp\n'
            '\t          > set thost=127.0.0.1 tport=1/8000\n'
            '\t          > set proto=tcp\n'
            '\t | Refer to [show] command to get options[/]\n')
            return 0

        elif command == 'unset':
            Console.print(f'[{FSUCCESS}]\n unset:\t Unassigns any value provided to the given option\n'
            '\t Usage: unset \[option1] \[option2] ...\n'
            '\t | Note: It also unassigns the values defined in \[config.py][/]\n')
            return 0

        elif command == 'about':
            Console.print(f'[{FSUCCESS}]\n about:\t Displays information about the provided module\n'
            '\t Usage: about \[module_name]\n'
            '\t\t | If no argument is provided it takes the selected module as argument[/]\n')
            return 0

        elif command == 'alias':
            Console.print(f'[{FSUCCESS}]\n alias:\t Set an alias for a command\n'
            '\t Usage: alias \[alias_name]<\[command]\n'
            '\t Example: > alias u<use\n'
            '\t          > u$\n'
            '\t          > alias thost<set thost\n'
            '\t          > thost$=127.0.0.1\n'
            '\t          > alias localhost<127.0.0.1\n'
            '\t          > set thost=$localhost$\n'
            '\t | If ran without argument it lists all the available aliases[/]\n')
            return 0

        elif command == 'unalias':
            Console.print(f'[{FSUCCESS}]\nunalias:\t Unset a pre-existing alias\n'
            '\t\t | Usage: unalias \[alias_name][/]\n')
            return 0

        elif command == 'use':
            Console.print(f'[{FSUCCESS}]\nuse: \t Use an available module\n'
            '\t Usage: use \[module_name]\n[/]')
            return 0

        elif command in ['exit', 'back', 'help', 'clear', 'run', 'list']:
            Console.print(f'[{FURGENT}]Please refer the default help for \'{command}\'[/]')
            return 3

        else:
            Console.print(f'[{FALERT}]Error: No such command: \'[bold]{command}[/]\'[/]')
            return 1

class Options():
    """List values assigned to various options of the module"""
    def __init__(self, MODULE, option_dict: dict):
        self.module = MODULE
        self.option_dict = option_dict
        self.modules = valid_modules

    def showoriginal(self, option: str) -> str:
        value = self.option_dict[option]['value']['value']
        _type = self.option_dict[option]['value']['type']
        if type(value) is not (list or dict or tuple):
            return str(value)
        
        for rule in self.option_dict[option]['typerules']:
            scheme: dict = self.option_dict[option]['typerules'][rule]
            if scheme.get('delimeter') and type(value) is list and _type == rule:
                delimeter : str = scheme.get('delimeter')
                return delimeter.join(value)

    def showOptions(self, trueval: bool = True):
        """
        Display values assigned to each options in a module.
        
        If no module is selected display values assigned to all options.
        """

        new_table = table.Table("Option", "Value", "Descrption", box=box.SIMPLE)

        if self.module in self.modules:
            COLOR: str = ""
            for option in self.modules[self.module]['options']:
                display_value = self.option_dict[option]['value'] if option in self.option_dict else "[red]***N/A***[/]"
                OptionIsRequired: bool = self.option_dict[option]['required'] is (not None and True) if option in self.option_dict else False
                if option in self.option_dict:
                    if self.option_dict[option]['type'] == "dict":
                        display_value = self.showoriginal(option) if not trueval else self.option_dict[option]['value']
                        if self.option_dict[option]['value']['value'] in [None, '']:
                            if OptionIsRequired:
                                COLOR = "red"
                            else:
                                COLOR = "yellow"
                        else:
                            COLOR = "white"
                    else:
                        if self.option_dict[option]['value'] in [None, '']:
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
                    self.option_dict.get(option).get('description') if self.option_dict.get(option) else '[red]***N/A***'
                )


        elif not self.module:
            for option in self.option_dict:
                display_value: str = str(self.option_dict[option]['value'] if option in self.option_dict else f"[red]*N/A*[/]")
                if self.option_dict[option]['type'] == "dict":
                    display_value = str(self.showoriginal(option) if not trueval else self.option_dict[option]['value'])
                
                new_table.add_row(option, display_value, self.option_dict.get(option).get('description'))
        
        Console.print(new_table)