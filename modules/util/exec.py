"""
Module containing the functions for execution,

- `run` function to run the assigned module,
- `set` function to assign a given value to the asked option,
- `unset` function to unassign values from an asked option.
"""

from modules.data.AboutList import moduleHelp
from config import colors, variables

FALERT = colors.FALERT
BALERT = colors.BALERT
BNORMAL = colors.BNORMAL


def run(module, options):
    """Function to run the assigned module"""
    import modules.probe.ports as ports
    import modules.probe.osprobe as osprobe
    if module in moduleHelp(module).modules:
        try:
            lhost    = options[0]
            lport    = options[1]
            protocol = options[2]
            timeout  = options[3]
            tryct    = options[4]
            nmap     = options[5]
            verbose  = options[6]
            threading= options[7]
            try:
                if lhost == '':
                    print(FALERT+'Error: Invalid value for LHOST')
                else:
                    if module == 'probe':
                        if lport == '':
                            print(FALERT+'Error: value for LPORT')

                        ports.display(lhost, lport, timeout, protocol, tryct, verbose, threading)
                        return 0

                    elif module == 'osprobe':
                        osprobe.checkOS(lhost, tryct, nmap).scanner()
                        return 0

            except Exception as e:
                print(e)
                return 1

        except KeyboardInterrupt:
            print(FALERT+'\nalert: KeyboardInterrupt detected\n')
            return 2

    else:
        print(f'{BALERT}[-] Error: Invalid module \'{module}\'{BNORMAL}')
        return 1

def set(option_list: list, option: str, value: str):
    """Function to assign a given value to the asked option."""

    if value and option != 'all':
        # if the first argument is 'all' all values default to those specified in config.py
        if option in ['THOST', 'thost']:
            print(f'THOST => {value}')
            option_list[0] = value

        elif option in ['TPORT', 'tport']:
            if '/' in value:
                option_list[1]['value'] = value.split('/')
                option_list[1]['type'] = 'range'
                display = option_list[1]['value']
                print(f'TPORT => {display}')

            elif ',' in value:
                option_list[1]['value'] = value.split(',')
                option_list[1]['type'] = 'group'
                display = option_list[1]['value']
                print(f'TPORT => {display}')


            else:
                print(f'TPORT => {value}')
                option_list[1]['value'] = int(value)
                option_list[1]['type'] = 'single'
                display = option_list[1]['value']
                print(f'TPORT => {display}')

        elif option in ['PROTO', 'proto', 'protocol', "PROTOCOL"]:
            print(f'PROTO => {value}')
            option_list[2] = value

        elif option in ['TMOUT', 'tmout']:
            print(f'TMOUT => {value}')
            option_list[3] = value

        elif option in ['TRYCT', 'tryct']:
            print(f'TRYCT => {value}')
            option_list[4] = int(value)

        elif option in ['NMAP', 'nmap']:
            print(f'NMAP  => {value}')
            option_list[5] = int(value)

        elif option in ['VERBOSE', 'verbose']:
            if value not in ['true', 'false']:
                print(FALERT+'Error: Invalid value provided')
            elif value == 'true':
                option_list[6] = True
                print(f'VERBOSE => {option_list[6]}')
            elif value == 'false':
                option_list[6] = False
                print(f'VERBOSE => {option_list[6]}')

        elif option in ['THREADING', 'threading']:
            if value not in ['true', 'True', 'false', 'False']:
                print(f'{FALERT}Error: Invalid value provided')
                option_list.append(1)
            elif value in ['true', 'True']:
                option_list[7] = True
            else:
                option_list[7] = False
            print(f'THREADING => {option_list[7]}')

        else:
            print(FALERT+'[-] Error: Invalid option')
            option_list.append(1)

    elif option == 'all':
        # If there are no values in the config.py then,
        # this is same as `unset all`
        option_list[0] = variables.THOST
        option_list[1] = variables.tport()
        option_list[2] = variables.PROTOCOL
        option_list[3] = variables.timeout()
        option_list[4] = variables.trycount()
        option_list[5] = variables.Nmap()
        option_list[6] = variables.Verbose()
        option_list[7] = variables.Threading()

    elif not value:
        print(f'{FALERT}[-] Error: no value provided to option')
        option_list.append(1)

    else:
        print(f"{FALERT}[-] Error: Invalid value provided to option")
        option_list.append(1)

    return option_list

def unset(option_list: list, option: str):
    """Function to unassign values from an asked option."""
    if option in ['THOST', 'thost']:
        print(f'{FALERT}unset THOST')
        option_list[0] = ''

    elif option in ['TPORT', 'tport']:
        print(f'{FALERT}unset TPORT')
        option_list[1]['value'] = ''
        option_list[1]['type'] = ''

    elif option in ['PROTO', 'proto', 'protocol', 'PROTOCOL']:
        print(f'{FALERT}unset PROTO')
        option_list[2] = ''

    elif option in ['TMOUT', 'tmout']:
        print(f'{FALERT}unset TMOUT')
        option_list[3] = 1

    elif option in ['TRYCT', 'tryct']:
        print(f'{FALERT}unset TRYCT')
        option_list[4] = 1

    elif option in ['NMAP', 'nmap']:
        print(f'{FALERT}unset NMAP')
        option_list[5] = 0

    elif option in ['VERBOSE', 'verbose']:
        print(f'{FALERT}unset VERBOSE')
        option_list[6] = ''

    elif option in ['THREADING', 'threading']:
        print(f'{FALERT}unset THREADING')
        option_list[7] = ''

    elif option == 'all':
        option_list[0] = ''
        option_list[1]['value'] = ''
        option_list[1]['type'] = ''
        option_list[2] = ''
        option_list[3] = 1
        option_list[4] = 1
        option_list[5] = 0
        option_list[6] = ''
        option_list[7] = ''
    else:
        print(FALERT+'Error: Invalid option')
        option_list.append(1)

    return option_list