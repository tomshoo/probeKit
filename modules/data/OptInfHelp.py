# This is the data-information module which will print help for the interpreter and information about selected module

from config import colors as colors
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
            '\t list\t\t prints available modules\n'+
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
            '\t\t | status: prints exit status of previous command[/]\n')
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

class Info():
    """List available options for a selected module"""
    def __init__(self, MODULE):
        self.module = MODULE

    def showInfo(self):
        """Display the options for available modules."""
        module = self.module

        if module == 'probe':
            Console.print(f'\n\t[*] THOST => hosts ip4 address (required) (THOST => thost)\n'
            f'\t[*] TPORT => ports to scan on host (required) (TPORT => tport)\n'
            f'[{FALERT}]\t             | values can be set as:[/]\n'
            f'\t                                   | \[portnumber] (single port scan)\n'
            f'\t                                   | \[startport/endport] (port range)\n'
            f'\t                                   | \[port1,port2,port3,...] (port group)\n\n'
            f'\t[*] PROTO => protocol to use for scanning (required) (PROTO => proto)\n'
            f'\t[{FALERT}]             | Available protocols:[/] \n'
            f'\t                                  | [TCP => tcp => TCP/IP => tcp/ip]\n'
            f'\t                                  | [UDP => udp]\n\n'
            f'\t[*] TMOUT => time to wait for incomming packet in seconds (set to \'1\' by default)(TMOUT => tmout)\n\n'
            f'\t[*] TRYCT => number of tries to perform while performing UDP scan (set to \'1\' by default)(TRYCT => tryct)\n\n'
            f'\t[*] VERBOSE => Provide a verbose output or not (VERBOSE => verbose)\n'
            f'\t[{FALERT}]                     | Available options are true (or) false\n\n[/]'
            f'\t[*] THREADING => Allow threading while scanning ports (THREADING => threading)\n'
            f'\t[{FALERT}]                     | Available options are true (or) false\n[/]')
            return 0

        elif module == 'osprobe':
            Console.print(f'\n\t[*] THOST => hosts ip4 address (required) (THOST => thost)\n\n'
            f'\t[*] TRYCT => number of tries to send the packet (set to \'1\' by default) (TRYC => tryc)\n\n'
            f'\t[*] NMAP  => should we perform an NMAP scan? (set to \'0\' by default) (NMAP => nmap)\n'
            f'\t[{FALERT}]           | 0 implies flase\n'
            f'\t           | 1 implies true\n'
            f'\t           | WARNING: Use at your own risk\n[/]')
            return 0

        elif module == 'dirfuzz':
            Console.print('\n\t[white]TURL     => Complete url of the target `http(s)://<domain name>/`\n'
            '\tMODE     => Type of brute forcing\n'
            '\t\t | subdomain: bruteforce the subdomain for the given url\n'
            '\t\t | directory: bruteforcing the directories in the given url\n'
            '\tWORDLIST => Path to a wordlist file\n'
            '\t\t | Path can be relative\n'
            '\t\t | Use proper structure for your operating system\n'
            '\t\t\t - `/` for *nix and `\\` for dos based systems\n'
            '\tDEPTH    => Depth to crawl if type is set to `directory`\n'
            '\tVERBOSE  => Display an expanded output if set to true[/]\n')
            return 0

        else:
            Console.print(f'[{FALERT}]Error: Invalid module[/]')
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