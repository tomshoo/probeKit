from config import valid_modules as _modules, colors as _colors
import modules.probe.ports as _ports
import modules.probe.osprobe as _osprobe
import modules.probe.fuzz as _fuzz
from rich import traceback, console
traceback.install()
Console = console.Console()

_FALERT = _colors.FALERT
_BALERT = _colors.BALERT

def run(module: str, options: dict) -> int:
    if module in _modules:
        try:
            if module == "ports":
                if not options['TPORT']['value']['value']:
                    Console.print(f'[bold {_FALERT}]Error: Invalid value for tport[/]')
                    return 1

                return _ports.portprobe(
                    options['THOST']['value'],
                    options['TPORT']['value'],
                    options['TIMEOUT']['value'],
                    options['PROTOCOL']['value'],
                    options['TRYCT']['value'],
                    options['VERBOSE']['value'],
                    options['THREADING']['value']
                ).display()
            elif module == "osprobe":
                return _osprobe.checkOS(
                    options['THOST']['value'],
                    options['TRYCT']['value'],
                    options['NMAP']['value']
                ).scanner()
            elif module == "fuzz":
                return _fuzz.fuzzer(
                    options['TURL']['value'],
                    options['MODE']['value'],
                    options['WORDLIST']['value'],
                    options['DEPTH']['value'],
                    options['VERBOSE']['value']
                ).fuzz()

            return 0
        except PermissionError as e:
            Console.print(f'[{_FALERT}]{str(e)}[/]')
            return 1

        except FileNotFoundError as e:
            Console.print(f'[{_FALERT}]{str(e)}[/]')
            return 1
    
    else:
        Console.print(f'[{_BALERT}][-] Error: Invalid module "{module}"[/]')
        return 1