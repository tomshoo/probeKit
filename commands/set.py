def run(option_list: list, option: str, value: str):
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
            if isFloat(value):
                print(f'TMOUT => {value}')
                option_list[3] = value
            else:
                print(f'{FALERT}Error: Invalid value provided')

        elif option in ['TRYCT', 'tryct']:
            if value.isdigit():
                print(f'TRYCT => {value}')
                option_list[4] = int(value)
            else:
                print(f'{FALERT}Error: Invalid value provided')

        elif option in ['NMAP', 'nmap']:
            if value.isdigit():
                print(f'NMAP  => {value}')
                option_list[5] = int(value)
            else:
                print(f'{FALERT}Error: Invalid value provided')

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
