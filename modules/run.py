#!/usr/bin/env python3
import modules.probe.ports as ports
from modules.data.OptInfHelp import PromptHelp, Options, Info
import modules.data.AboutList as aboutList
import modules.probe.osprobe as osprobe

def run(module, options):
    try:
        lhost    = options[0]
        lport    = options[1]
        protocol = options[2]
        timeout  = options[3]
        tryct    = options[4]
        nmap     = options[5]
        verbose  = options[6]
        try:
            if lhost == '':
                print(FALERT+'Error: Invalid value for LHOST')
            else:
                if module == 'probe':
                    if lport == '':
                        raise Exception(FALERT+'Error: value for LPORT')

                    ports.scanner(lhost, lport, timeout, protocol, tryct, verbose)

                elif module == 'osprobe':
                    osprobe.checkOS(lhost, tryct, nmap).scanner()

        except Exception as e:
            print(e)

    except KeyboardInterrupt:
        print(FALERT+'\nalert: KeyboardInterrupt detected\n')