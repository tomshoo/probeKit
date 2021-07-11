#! /usr/bin/env python3

# This is the data-information module which will print help for the interpreter and information about selected module

import sys
sys.path.append('../../')
from config import colors

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL

# This class prints help for the interpreter
class Help():
    def __init__(self, MODULE):
        self.module = MODULE

    def showHelp(self):
        module = self.module

        # Checks whether the shell is module interpreter or module selector session
        if module == '':
            print(FSUCCESS+'\nUsage: [verb] [options]')
            print('Available verbs are: use, help, exit, terminate, clear\n')
            print('\t use\t\t specify a module to use\n\t\t\t | usage: use [module]\n')
            print('\t help\t\t prints this help message\n')
            print('\t list\t\t prints available modules\n')
            print('\t about\t\t prints details about specified module\n\t\t\t | Usage: about [moduleName]\n')
            print('\t exit\t\t exits the interpreter\n')
            print('\t terminate\t alias for exit\n')
            print('\t clear\t\t clears screen\n\t\t\t | usage: clear [option]\n\t\t\t | available options are: exit, terminate\n')
            print('\t banner\t\t prints an ascii banner\n')

        else:
            print(FSUCCESS+'\nUsage: [verb] [options]')
            print('Available verbs are: set, help, exit, back, info, options, clear, getstat, run\n')
            print('\t options\t lists available options to configure\n')
            print('\t info\t\t shows values assigned to each option\n')
            print('\t set\t\t assignes values to available options\n\t\t\t | usage: set [option] [value]\n')
            print('\t help\t\t prints this help message\n')
            print('\t exit\t\t exits the whole interpreter\n')
            print('\t back\t\t moves back to the module selector\n')
            print('\t getstat\t prints the status of previous verb\n')
            print('\t clear\t\t clears screen\n')
            print('\t run\t\t runs the selected module\n')
            print('\t about\t\t prints details about specified module\n\t\t\t | Usage: about [moduleName]\n')
            print('\t list\t\t prints available modules\n')
            print('\t banner\t\t prints an ascii banner\n')

# List available options for a selected module
class Options():
    def __init__(self, MODULE):
        self.module = MODULE

    def showOptions(self):
        module = self.module

        if module == 'probe':
            print(f'\n\t[*] LHOST => hosts ip4 address(required)(LHOST => lhost)')
            print(f'\t[*] LPORT => ports to scan on host(required)(LPORT => lport)')
            print(FALERT+f'\t             | values can be set as [portnumber(single portscan)] or [startport/endport(multiple portscan)]\n')
            print(FNORMAL+f'\t[*] PROTO => protocol to use for scanning(required)(PROTO => proto)')
            print(FALERT+f'\t             | Available protocols: ')
            print(f'\t                                  | [TCP => tcp => TCP/IP => tcp/ip]')
            print(f'\t                                  | [UDP => udp]\n')
            print(FNORMAL+f'\t[*] TMOUT => time to wait for incomming packet in seconds(set to \'1\' by default)(TMOUT => tmout)\n')
            print(FNORMAL+f'\t[*] TRYCT => number of tries to perform while performing UDP scan(set to \'1\' by default)(TRYCT => tryct)\n')
            print(FNORMAL+f'\t[*] VERBOSE => Provide a verbose output or not(VERBOSE => verbose)')
            print(f'\t                     | Available options are true (or) false\n')

        elif module == 'osprobe':
            print(f'\n\t[*] LHOST => hosts ip4 address(required)(LHOST => lhost)\n')
            print(f'\t[*] TRYCT => number of tries to send the packet(set to \'1\' by default)(TRYC => tryc)\n')
            print(f'\t[*] NMAP  => should we perform an NMAP scan?(set to \'0\' by default)(NMAP => nmap)')
            print(f'\t           {FALERT}| 0 implies flase')
            print(f'\t           | 1 implies true')
            print(f'\t           | WARNING: Use at your own risk{FNORMAL}\n')

        else:
            raise Exception(FALERT+'Error: Invalid module')

# List values assigned to various options of the module
class Info():
    def __init__(self, MODULE, OPTIONS):
        self.module  = MODULE
        self.lhost   = OPTIONS[0]
        self.lport   = OPTIONS[1]
        self.proto   = OPTIONS[2]
        self.timeout = OPTIONS[3]
        self.tryct = OPTIONS[4]
        self.nmap = OPTIONS[5]
        self.verbose = OPTIONS[6]

    def showInfo(self):
        if self.module == 'probe':
            if self.lhost != '':
                print(FSUCCESS+'\n\t[+] '+f'LHOST => {self.lhost}')
            else:
                print(FALERT+'\n\t[-] '+f'LHOST => {self.lhost}')

            if self.lport != '':
                print(FSUCCESS+f'\t[+] '+f'LPORT => {self.lport}')
            else:
                print(FALERT+'\t[-] '+f'LPORT => {self.lport}')

            if self.proto != '':
                print(FSUCCESS+'\t[+] '+f'PROTO => {self.proto}')
            else:
                print(FALERT+'\t[-] '+f'PROTO => {self.proto}')

            print(FSUCCESS+f'\t[*] TRYCT => {self.tryct}')

            print(FSUCCESS+f'\t[*] TMOUT => {self.timeout}')

            if self.verbose != '':
                print(FSUCCESS+'\t[+] '+f'VERBOSE => {self.verbose}\n')
            else:
                print(FALERT+'\t[-] '+f'VERBOSE => {self.verbose}\n')


        elif self.module == 'osprobe':
            if self.lhost != '':
                print(FSUCCESS+'\n\t[+] '+f'LHOST => {self.lhost}')
            else:
                print(FALERT+'\n\t[+] '+f'LHOST => {self.lhost}')

            print(FSUCCESS+'\t[+] '+f'NMAP  => {self.nmap}')
            print(FSUCCESS+f'\t[*] TRYCT => {self.tryct}\n')

        else:
            raise Exception(FALERT+'Error: Invalid module')
