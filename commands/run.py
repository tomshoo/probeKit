from modules.data.AboutList import moduleHelp
from config import colors, variables
from modules.util.utils import isFloat

FALERT = colors.FALERT
BALERT = colors.BALERT
BNORMAL = colors.BNORMAL


def run(module, options) -> int:
    """Function to run the assigned module"""
    import modules.probe.ports as ports
    import modules.probe.osprobe as osprobe
    if module in moduleHelp(module).modules:
        thost    = options[0]
        tport    = options[1]
        protocol = options[2]
        timeout  = options[3]
        tryct    = options[4]
        nmap     = options[5]
        verbose  = options[6]
        threading= options[7]
        if thost == '':
            print(FALERT+'Error: Invalid value for THOST')
        else:
            if module == 'probe':
                if tport == '':
                    print(FALERT+'Error: Invalid value for TPORT')

                ports.display(thost, tport, timeout, protocol, tryct, verbose, threading)
                return 0

            elif module == 'osprobe':
                osprobe.checkOS(thost, tryct, nmap).scanner()
                return 0

    else:
        print(f'{BALERT}[-] Error: Invalid module \'{module}\'{BNORMAL}')
        return 1