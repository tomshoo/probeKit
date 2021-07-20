#! /usr/bin/env python3

import sys
sys.path.append('../../')
from config import colors

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL

class moduleHelp():

    modules = ['probe', 'osprobe']

    def __init__(self, MODULE):
        self.module = MODULE

    def listmodules(self):
        # Checks if there is any active module
        if self.module != '':
            print('Currently activated module: '+FALERT+f'[{self.module}]')

        print(FNORMAL+'Available modules are:')
        for x in self.modules:
            print(FSUCCESS+"\t", x)

        print(FNORMAL+'type: about [Module] for more information')

    # Prints data about a give module will print data without argument if a module is active
    def aboutModule(self, moduleName):
        if moduleName == 'probe':
            print(FALERT+f'\nName:\t\t{moduleName}')
            print('Type:\t\tRecon')
            print('Description:\tThis module is meant to perform a basic port scan on the specidied host.\n')
            print(FSUCCESS+'Available options:\n')
            print('\tLHOST => IPv4 address or domain name of the target host')
            print('\t\t | Can be called LHOST or lhost\n')
            print('\tLPORT => ports to be scanned')
            print('\t\t | Can be called LPORT or lport')
            print('\t\t | Specify single port as `set lport [portnumber]`')
            print('\t\t | or set multiple ports by `set lport [startPort]/[endPort]`\n')
            print('\tTMOUT => timeout duration while awaiting connection')
            print('\t\t | Can be called TMOUT or tmout')
            print('\t\t | Defaults to 1 second duration\n')
            print('\tPROTO => Protocol to be used to scan')
            print('\t\t | Can be called PROTO or proto')
            print('\t\t | Available Protocols are:')
            print('\t\t                          | TCP => TCP/IP(tcp => tcp/ip)')
            print('\t\t                          | UDP(udp)\n')
            print('\tVERBOSE => show complete output')
            print('\t\t | Available Options are true/false\n')

        elif moduleName == 'osprobe':
            print(FALERT+f'\nName:\t\t{moduleName}')
            print('Type:\t\tRecon')
            print('Description:\tThis module sends a basic ICMP packet to a host to determine its OS')
            print('            \t| This module does not confirm the OS since it is just using TTL within the ICMP response\n')
            print(FSUCCESS+'Available options:\n')
            print('\tLHOST => IPv4 address or domain name of the target host')
            print('\t\t | Can be called LHOST or lhost\n')
            print('\tTRYCT => Number of times ICMP packet must be sent')
            print('\t\t | Set to 1 packet by default')
            print('\t\t | Can be called TRYCT ot tryct\n')
            print('\tNMAP  => Run an nmap scan')
            print('\t\t | 0 for false')
            print('\t\t | 1 for true')
            print(f'{FALERT}\t\t | Warning: It is an active scanning method hence use it on your own risk\n')

        elif moduleName == '':
            print(FALERT+'[-] Error: no module selected')

        else:
            print(f'{FALERT}[-] Error: Invalid module \'{moduleName}\'')
