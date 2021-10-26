from config import (
    colors as _colors,
    valid_modules as _modules,
)
import modules.probe.ports as _ports
import modules.probe.osprobe as _osprobe
import modules.probe.dirfuzz as _dirfuzz

_FALERT = _colors.FALERT
_BALERT = _colors.BALERT
_BNORMAL = _colors.BNORMAL

def run(module: str, options: dict) -> int:
    if module in _modules:
        try:
            if module == "probe":
                if not options['tport']['value']['value']:
                    print(f'{_FALERT}Error: Invalid value for tport')
                    return 1

                _ports.display(
                    options['thost']['value'],
                    options['tport']['value'],
                    options['timeout']['value'],
                    options['protocol']['value'],
                    options['tryct']['value'],
                    options['verbose']['value'],
                    options['threading']['value']
                )
            elif module == "osprobe":
                _osprobe.checkOS(
                    options['thost']['value'],
                    options['tryct']['value'],
                    options['nmap']['value']
                ).scanner()
            elif module == "dirfuzz":
                _dirfuzz.fuzz(
                    options['turl']['value'],
                    options['wordlist']['value'],
                    options['depth']['value']
                )

            return 0
        except PermissionError as e:
            print(_FALERT, e)
            return 1

        except FileNotFoundError as e:
            print(_FALERT ,e)
            return 1
    
    else:
        print(f'{_BALERT}[-] Error: Invalid module \'{module}\'{_BNORMAL}')
        return 1