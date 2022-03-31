# This is the data-information module which will print help for the interpreter and information about selected module

from config import colors
from rich import traceback, console
Console = console.Console()
traceback.install()

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FURGENT = colors.FURGENT

class Help():
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
            '\t set\t\t (*)assignes aliases and available options\n'+
            '\t unset\t\t (*)unassigns given alias or option\n'+
            '\t help\t\t prints this help message\n'+
            '\t exit\t\t exits the whole interpreter\n'+
            '\t back\t\t moves back to the module selector\n'+
            '\t clear\t\t clears screen\n'+
            '\t run\t\t runs the selected module\n'+
            '\t about\t\t (*)prints details about specified module\n'+
            '\t banner\t\t prints an ascii banner\n'+
            '\nRun help \[command] for more information:\n'+
            '\t -> only the commands marked with (*) have a seperate help[/]\n'
            )
            return 0

        elif command == 'show':
            Console.print(f'[{FSUCCESS}]\n show:\t Shows information on provided argument\n'
            '\t Usage: show [argument] [module name (optional if argument is options and no module is selected by default)]\n'
            '\t Available arguments are:\n'
            '\t\t | options: shows values assigned to the options available for the selected module\n'
            '\t\t\t - shows all assigned values if no module is selected\n\n'
            '\t\t | info: shows available options for selected module\n'
            '\t\t | status: prints exit status of previous command\n'
            '\t\t | modules: list all available modules\n'
            '\t\t | aliases: list defined aliases\n'
            '\t\t | macros: list all defined macros[/]\n')
            return 0

        elif command == 'set':
            Console.print(f'[{FSUCCESS}]\n set:\t Sets options or aliases\n'
            '\t Usage: set \[option or alias or macro] \[key]=\[value]\n'
            '\t\t Set options,\n'
            '\t\t\t set option \[option_name]=\[option_value]\n'
            '\n'
            '\t\t Set aliases,\n'
            '\t\t\t set alias \[alias]=\[command]\n'
            '\t\t\t set alias \[alias]="\[long and complicated command]"\n'
            '\t\t Set macro,\n',
            '\t\t\t set macro \[macro]=\[macro_value]\n'
            f'\t\t\t *note: [{FALERT}]macro accepts only one key value pair at once.[/]\n',
            f'\t\t\t    [{FALERT}]Definition of multiple macros is not supported nor recommended.[/]\n'
            ## Well Console.print() straight up refused to work properly from this point in this statement...
            f'[{FSUCCESS}]\t\t\t - Then call macros via `$(macro) or $macro`[/]\n',
            f'[{FSUCCESS}]\t\t\t -> Difference between $(macro) and $macro is:\n[/]',
            f'[{FSUCCESS}]\t\t\t\t - $(macro) allows tu use the macro name as value if the macro is not found\n[/]',
            f'[{FSUCCESS}]\t\t\t\t - $macro on other hand does not allow using macro name as a value\n[/]')
            return 0

        elif command == 'unset':
            Console.print(f'[{FSUCCESS}]\n unset:\t Unassigns any value provided to the given option\n'
            '\t Usage: unset \[option or alias or macro] \[key1] \[key2]...\[keyN]\n'
            '\t | Note: It also unassigns any of the values defined in `UserConfig.py`[/]\n')
            return 0

        elif command == 'about':
            Console.print(f'[{FSUCCESS}]\n about:\t Displays information about the provided module\n'
            '\t Usage: about \[module_name]\n'
            '\t\t | If no argument is provided it takes the selected module as argument[/]\n')
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