from config import valid_modules as _modules, colors as _colors
import modules.probe.ports as _ports
import modules.probe.osprobe as _osprobe
import modules.probe.fuzz as _fuzz
from rich import traceback, console
from modules.util.CommandUtils.ReturnStructure import RetObject
traceback.install()
Console = console.Console()

_FALERT = _colors.FALERT
_BALERT = _colors.BALERT

def run(_arguments, ReturnObject: RetObject) -> RetObject:
    module = ReturnObject.module
    options = ReturnObject.option_dict
    if module in _modules:
        try:
            if module == "ports":
                if not options['tport']['value']['value']:
                    Console.print(f'[bold {_FALERT}]Error: Invalid value for tport[/]')
                    ReturnObject.exit_code = 1
                else:
                    ReturnObject.exit_code = _ports.portprobe(
                        options['thost']['value'],
                        options['tport']['value'],
                        options['timeout']['value'],
                        options['protocol']['value'],
                        options['tryct']['value'],
                        options['verbose']['value'],
                        options['threading']['value']
                    ).display()
            elif module == "osprobe":
                ReturnObject.exit_code = _osprobe.checkOS(
                    options['thost']['value'],
                    options['tryct']['value'],
                    options['nmap']['value']
                ).scanner()
            elif module == "fuzz":
                ReturnObject.exit_code = _fuzz.fuzzer(
                    options['turl']['value'],
                    options['mode']['value'],
                    options['wordlist']['value'],
                    options['depth']['value'],
                    options['verbose']['value']
                ).fuzz()

            return ReturnObject
        except PermissionError as e:
            Console.print(f'[{_FALERT}]{str(e)}[/]')
            ReturnObject.exit_code = 1

        except FileNotFoundError as e:
            Console.print(f'[{_FALERT}]{str(e)}[/]')
            ReturnObject.exit_code = 1
        
        return ReturnObject
    
    else:
        Console.print(f'[{_BALERT}][-] Error: Invalid module "{module}"[/]')
        ReturnObject.exit_code = 1
        return ReturnObject