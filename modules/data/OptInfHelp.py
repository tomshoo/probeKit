#! /usr/bin/env python3

# This is the data-information module which will print help for the interpreter and information about selected module

from config import colors

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL
FURGENT = colors.FURGENT

# This class prints help for the interpreter
class PromptHelp():
    def __init__(self, command : str):
        self.command = command

    def showHelp(self):
        command = self.command

        # Checks whether the shell is module interpreter or module selector session
        if command == '':
            print(FSUCCESS+'\nUsage: [verb] [options]')
            print('Available verbs are: set, help, exit, back, clear, run\n')
            print('\t show\t\t shows information on provided argument(*)\n')
            print('\t set\t\t assignes values to available options(*)\n')
            print('\t help\t\t prints this help message\n')
            print('\t exit\t\t exits the whole interpreter\n')
            print('\t back\t\t moves back to the module selector\n')
            print('\t clear\t\t clears screen\n')
            print('\t run\t\t runs the selected module\n')
            print('\t about\t\t prints details about specified module(*)\n')
            print('\t list\t\t prints available modules\n')
            print('\t banner\t\t prints an ascii banner\n')
            print('\t alias\t\t set an alias for a command(*)\n')
            print('\t unalias\t unset a pre-existing alias(*)\n')
            return 0

        elif command == 'show':
            print(f'{FSUCCESS}\n show:\t shows information on provided argument')
            print('\t Usage: show [argument]')
            print('\t | Available arguments are:')
            print('\t\t | info: shows values assigned to the options available for the selected module')
            print('\t\t\t | shows all assigned values if no module is selected\n')
            print('\t\t | options: shows available options for selected module\n')
            print('\t\t | status: prints exit status of previous command\n')
            return 0

        elif command == 'set':
            print(f'{FSUCCESS}\n set:\t sets the provided value to the provided option')
            print('\t | Usage: set [option] [value]')
            print('\t | refer the [show] command to get options\n')
            return 0

        elif command == 'about':
            print(f'{FSUCCESS}\n about:\t displays information about the provided module')
            print('\t Usage: about [module_name]')
            print('\t\t | If no argument is provided it takes the selected module as argument\n')
            return 0

        elif command == 'alias':
            print(f'{FSUCCESS}\n alias:\t set an alias for a command')
            print('\t Usage: alias [alias_name]=[command]')
            print('\t Example: > alias lhost=set lhost')
            print('\t          > lhost 127.0.0.1')
            print('\t | If ran without argument it lists all the available aliases\n')
            return 0

        elif command == 'unalias':
            print(f'{FSUCCESS}\nunalias:\t unset a pre-existing alias')
            print('\t\t | Usage: unalias [alias_name]\n')
            return 0

        elif command in ['exit', 'back', 'help', 'clear', 'run', 'list']:
            print(f'{FURGENT}Please refer the default help for \'{command}\'')
            return 3

        else:
            print(f'{FALERT}Error: No such command: \'{command}\'')
            return 1


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
            return 0

        elif module == 'osprobe':
            print(f'\n\t[*] LHOST => hosts ip4 address(required)(LHOST => lhost)\n')
            print(f'\t[*] TRYCT => number of tries to send the packet(set to \'1\' by default)(TRYC => tryc)\n')
            print(f'\t[*] NMAP  => should we perform an NMAP scan?(set to \'0\' by default)(NMAP => nmap)')
            print(f'\t           {FALERT}| 0 implies flase')
            print(f'\t           | 1 implies true')
            print(f'\t           | WARNING: Use at your own risk{FNORMAL}\n')
            return 0

        else:
            print(FALERT+'Error: Invalid module')
            return 1

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
                print(FALERT+'\n\t[-] '+f'LHOST => {self.lhost}')

            print(FSUCCESS+'\t[+] '+f'NMAP  => {self.nmap}')
            print(FSUCCESS+f'\t[*] TRYCT => {self.tryct}\n')

        else:
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

            if self.verbose != '':
                print(FSUCCESS+'\t[+] '+f'VERBOSE => {self.verbose}')
            else:
                print(FALERT+'\t[-] '+f'VERBOSE => {self.verbose}')

            print(FSUCCESS+'\t[+] '+f'NMAP  => {self.nmap}')
            print(FSUCCESS+f'\t[*] TRYCT => {self.tryct}')
            print(FSUCCESS+f'\t[*] TMOUT => {self.timeout}\n')
