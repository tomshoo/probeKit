
def run(option_list: list, option: str):
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