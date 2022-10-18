from config import valid_modules as _modules, colors as _colors
import modules.probe.ports as _ports
import modules.probe.osprobe as _osprobe
import modules.probe.fuzz as _fuzz
from rich import traceback, console
from modules.util.CommandUtils.ReturnStructure import RetObject

from . import Runnable

traceback.install()
Console = console.Console()

_FALERT = _colors.FALERT
_BALERT = _colors.BALERT


class RunModule(Runnable):
    def run(self) -> RetObject:
        module = self.retobj.module
        options = self.retobj.option_dict
        if module in _modules:
            try:
                if module == "ports":
                    if not options['tport']['value']['value']:
                        Console.print(
                            f'[bold {_FALERT}]Error: Invalid value for tport[/]')
                        self.retobj.exit_code = 1
                    else:
                        self.retobj.exit_code = _ports.portprobe(
                            options['thost']['value'],
                            options['tport']['value'],
                            options['timeout']['value'],
                            options['protocol']['value'],
                            options['tryct']['value'],
                            options['verbose']['value'],
                            options['threading']['value']
                        ).display()
                elif module == "osprobe":
                    self.retobj.exit_code = _osprobe.checkOS(
                        options['thost']['value'],
                        options['tryct']['value'],
                        options['nmap']['value']
                    ).scanner()
                elif module == "fuzz":
                    self.retobj.exit_code = _fuzz.fuzzer(
                        options['turl']['value'],
                        options['mode']['value'],
                        options['wordlist']['value'],
                        options['depth']['value'],
                        options['verbose']['value']
                    ).fuzz()

                return self.retobj
            except PermissionError as e:
                Console.print(f'[{_FALERT}]{str(e)}[/]')
                self.retobj.exit_code = 1

            except FileNotFoundError as e:
                Console.print(f'[{_FALERT}]{str(e)}[/]')
                self.retobj.exit_code = 1

            return self.retobj

        else:
            Console.print(
                f'[{_BALERT}][-] Error: Invalid module "{module}"[/]')
            self.retobj.exit_code = 1
            return self.retobj
