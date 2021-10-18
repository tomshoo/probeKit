from modules.data.AboutList import moduleHelp as _modulehelp
from config import colors as _colors
import modules.probe.ports as _ports
import modules.probe.osprobe as _osprobe
import modules.probe.dirfuzz as _dirfuzz

_FALERT = _colors.FALERT
_BALERT = _colors.BALERT
_BNORMAL = _colors.BNORMAL

def run(module, options) -> int:
    """Function to run the assigned module"""

    if module in _modulehelp(module).modules:
        thost    = options[0]
        tport    = options[1]
        protocol = options[2]
        timeout  = options[3]
        tryct    = options[4]
        nmap     = options[5]
        verbose  = options[6]
        threading= options[7]
        wordlist = options[8]

        if thost == '':
            print(_FALERT+'Error: Invalid value for THOST')
            return 1

        else:
            try:
                if module == 'probe':
                    if tport == '':
                        print(_FALERT+'Error: Invalid value for TPORT')
                        return 1

                    _ports.display(thost, tport, timeout, protocol, tryct, verbose, threading)

                elif module == 'osprobe':
                    _osprobe.checkOS(thost, tryct, nmap).scanner()

                elif module == 'dirfuzz':
                    _dirfuzz.fuzz(thost, wordlist, tryct)
            except PermissionError as e:
                print(e)
                return 1
            except FileNotFoundError as e:
                print(e)
                return 1

            finally:
                return 0

    else:
        print(f'{_BALERT}[-] Error: Invalid module \'{module}\'{_BNORMAL}')
        return 1
