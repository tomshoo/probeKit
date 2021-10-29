# This is the data-information module which will print help for the interpreter and information about selected module

from config import colors
from platform import platform
from rich import traceback, table, box, console
Console = console.Console()
traceback.install()

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL
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
            print(FSUCCESS+'\nUsage: [verb] [options]')
            print('Available verbs are:\n')
            print('\t use\t\t use an available module(*)')
            print('\t show\t\t shows information on provided argument(*)')
            print('\t set\t\t assignes values to available options(*)')
            print('\t unset\t\t unassigns value from the provided option(*)')
            print('\t help\t\t prints this help message')
            print('\t exit\t\t exits the whole interpreter')
            print('\t back\t\t moves back to the module selector')
            print('\t clear\t\t clears screen')
            print('\t run\t\t runs the selected module')
            print('\t about\t\t prints details about specified module(*)')
            print('\t list\t\t prints available modules')
            print('\t banner\t\t prints an ascii banner')
            print('\t alias\t\t set an alias for a command(*)')
            print('\t unalias\t unset a pre-existing alias(*)')
            print('\nRun help [command] for more information:')
            print('\t -> only the commands marked with (*) have a seperate help\n')
            return 0

        elif command == 'show':
            print(f'{FSUCCESS}\n show:\t Shows information on provided argument')
            print('\t Usage: show [argument]')
            print('\t Available arguments are:')
            print('\t\t | options: shows values assigned to the options available for the selected module')
            print('\t\t\t - shows all assigned values if no module is selected\n')
            print('\t\t | info: shows available options for selected module\n')
            print('\t\t | status: prints exit status of previous command\n')
            return 0

        elif command == 'set':
            print(f'{FSUCCESS}\n set:\t Sets the provided value to the provided option')
            print('\t Usage: set [option1]=[value1] [option2]=[value2] ...')
            print('\t Example: > set thost=127.0.0.1 tport=443,5432,8000 proto=tcp')
            print('\t          > set thost=127.0.0.1 tport=1/8000')
            print('\t          > set proto=tcp')
            print('\t | Refer to [show] command to get options\n')
            return 0

        elif command == 'unset':
            print(f'{FSUCCESS}\n unset:\t Unassigns any value provided to the given option')
            print('\t Usage: unset [option1] [option2] ...')
            print('\t | Note: It also unassigns the values defined in [config.py]\n')
            return 0

        elif command == 'about':
            print(f'{FSUCCESS}\n about:\t Displays information about the provided module')
            print('\t Usage: about [module_name]')
            print('\t\t | If no argument is provided it takes the selected module as argument\n')
            return 0

        elif command == 'alias':
            print(f'{FSUCCESS}\n alias:\t Set an alias for a command')
            print('\t Usage: alias [alias_name]<-[command]')
            print('\t Example: > alias u<use')
            print('\t          > u$')
            print('\t          > alias thost<set thost')
            print('\t          > thost$=127.0.0.1')
            print('\t          > alias localhost<127.0.0.1')
            print('\t          > set thost=$localhost$')
            print('\t | If ran without argument it lists all the available aliases\n')
            return 0

        elif command == 'unalias':
            print(f'{FSUCCESS}\nunalias:\t Unset a pre-existing alias')
            print('\t\t | Usage: unalias [alias_name]\n')
            return 0

        elif command == 'use':
            print(f'{FSUCCESS}\nuse: \t Use an available module')
            print('\t Usage: use [module_name]\n')
            return 0

        elif command in ['exit', 'back', 'help', 'clear', 'run', 'list']:
            print(f'{FURGENT}Please refer the default help for \'{command}\'')
            return 3

        else:
            print(f'{FALERT}Error: No such command: \'{command}\'')
            return 1


class Info():
    """List available options for a selected module"""
    def __init__(self, MODULE):
        self.module = MODULE

    def showInfo(self):
        """Display the options for available modules."""
        module = self.module

        if module == 'probe':
            print(f'\n\t[*] THOST => hosts ip4 address(required)(THOST => thost)')
            print(f'\t[*] TPORT => ports to scan on host(required)(TPORT => tport)')
            print(FALERT+f'\t             | values can be set as:')
            print('\t                                   | [portnumber] (single port scan)')
            print('\t                                   | [startport/endport] (port range)')
            print('\t                                   | [port1,port2,port3,...] (port group)\n')
            print(FNORMAL+f'\t[*] PROTO => protocol to use for scanning(required)(PROTO => proto)')
            print(FALERT+f'\t             | Available protocols: ')
            print(f'\t                                  | [TCP => tcp => TCP/IP => tcp/ip]')
            print(f'\t                                  | [UDP => udp]\n')
            print(FNORMAL+f'\t[*] TMOUT => time to wait for incomming packet in seconds(set to \'1\' by default)(TMOUT => tmout)\n')
            print(FNORMAL+f'\t[*] TRYCT => number of tries to perform while performing UDP scan(set to \'1\' by default)(TRYCT => tryct)\n')
            print(FNORMAL+f'\t[*] VERBOSE => Provide a verbose output or not(VERBOSE => verbose)')
            print(f'\t                     | Available options are true (or) false\n')
            print(f'{FNORMAL}\t[*] THREADING => Allow threading while scanning ports(THREADING => threading)')
            print(f'\t                     | Available options are true (or) false\n')
            return 0

        elif module == 'osprobe':
            print(f'\n\t[*] THOST => hosts ip4 address(required)(THOST => thost)\n')
            print(f'\t[*] TRYCT => number of tries to send the packet(set to \'1\' by default)(TRYC => tryc)\n')
            print(f'\t[*] NMAP  => should we perform an NMAP scan?(set to \'0\' by default)(NMAP => nmap)')
            print(f'\t           {FALERT}| 0 implies flase')
            print(f'\t           | 1 implies true')
            print(f'\t           | WARNING: Use at your own risk{FNORMAL}\n')
            return 0

        else:
            print(FALERT+'Error: Invalid module')
            return 1

class Options():
    """List values assigned to various options of the module"""
    def __init__(self, MODULE, option_dict: dict, modules: dict):
        self.module = MODULE
        self.option_dict = option_dict
        self.modules = modules

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
                display_value = self.option_dict[option]['value'] if option in self.option_dict else "***N/A***"
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
                new_table.add_row(f"[{COLOR}]{option}[/]", f"[white]{display_value}", self.option_dict.get(option).get('description'))


        elif not self.module:
            for option in self.option_dict:
                display_value: str = str(self.option_dict[option]['value'] if option in self.option_dict else f"{FALERT}*N/A*")
                if self.option_dict[option]['type'] == "dict":
                    display_value = str(self.showoriginal(option) if not trueval else self.option_dict[option]['value'])
                
                new_table.add_row(option, display_value, self.option_dict.get(option).get('description'))
        
        Console.print(new_table)