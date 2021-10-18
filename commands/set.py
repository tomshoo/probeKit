from config import colors as _colors, variables as _variables
from modules.util.utils import trim as _trim, args as _args

_FALERT = _colors.FALERT

class set_class:
    def __init__(self, option_list: list, options: list):
        ret_list: list = [option_list, 0]
        self.ret_list = ret_list
        self.options = options

    def run(self) -> list:
        options: str = ' '.join(self.options)

        if ' ' in options:
            assignment = options.split(' ')
            for data in assignment:
                option = _args(data.split('='), 0)
                value = _args(data.split('='), 1)
                self.assign(option, value)

        else:
            options = options.split('=')
            option = _args(options, 0)
            value = _args(options, 1)

            self.assign(_trim(option), _trim(value))

        return self.ret_list

    def assign(self, option: str, value: str) -> None:
        """Function to assign a given value to the asked option."""

        option_list = self.ret_list[0]
        exit_code = self.ret_list[1]
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
                    print(f'{_FALERT}Error: Invalid value provided')
                    exit_code=1

            elif option in ['TRYCT', 'tryct']:
                if value.isdigit():
                    print(f'TRYCT => {value}')
                    option_list[4] = int(value)

                else:
                    print(f'{_FALERT}Error: Invalid value provided')
                    exit_code=1

            elif option in ['NMAP', 'nmap']:
                if value.isdigit():
                    print(f'NMAP  => {value}')
                    option_list[5] = int(value)

                else:
                    print(f'{_FALERT}Error: Invalid value provided')
                    exit_code=1

            elif option in ['VERBOSE', 'verbose']:
                if value not in ['true', 'false']:
                    print(_FALERT+'Error: Invalid value provided')
                    exit_code=1

                elif value == 'true':
                    option_list[6] = True
                    print(f'VERBOSE => {option_list[6]}')

                elif value == 'false':
                    option_list[6] = False
                    print(f'VERBOSE => {option_list[6]}')

            elif option in ['THREADING', 'threading']:
                if value not in ['true', 'True', 'false', 'False']:
                    print(f'{_FALERT}Error: Invalid value provided')
                    exit_code = 1

                elif value in ['true', 'True']:
                    option_list[7] = True

                else:
                    option_list[7] = False

                print(f'THREADING => {option_list[7]}')

            elif option in ['WORDLIST', 'wordlist']:
                option_list[8] = value
                print(f'WORDLIST => {option_list[8]}')

            else:
                print(_FALERT+'[-] Error: Invalid option ', option)
                exit_code = 1

        elif option == 'all':
            # If there are no values in the config.py then,
            # this is same as `unset all`
            option_list[0] = _variables.THOST
            option_list[1] = _variables.tport()
            option_list[2] = _variables.PROTOCOL
            option_list[3] = _variables.timeout()
            option_list[4] = _variables.trycount()
            option_list[5] = _variables.Nmap()
            option_list[6] = _variables.Verbose()
            option_list[7] = _variables.Threading()

        elif not value:
            print(f'{_FALERT}[-] Error: no value provided to option')
            exit_code = 1

        else:
            print(f"{_FALERT}[-] Error: Invalid value provided to option")
            exit_code = 1

        self.ret_list[0] = option_list
        self.ret_list[1] = exit_code
