from config import colors as _colors

_FALERT = _colors.FALERT

class set_class:
    def __init__(self, option_list: list, options: list):
        option_list.append(0)
        self.option_list = option_list
        self.options = options
        
    def run(self):
        options: str = ' '.join(self.options)
        try:
            if ' ' in options:
                assignment = options.split(' ')
                for data in assignment:
                    option = data.split('=')[0]
                    value = data.split('=')[1]
                    self.assign(option, value)
            else:
                options = options.split('=')
                self.assign(options[0], options[1])
        
        except IndexError:
            print(f'{_FALERT}Error: Something went wrong!! Please check your syntax')
            self.option_list[8] = 1
        
        finally:
            return self.option_list
        
    def assign(self, option: str, value: str):
        """Function to assign a given value to the asked option."""

        if value and option != 'all':
            # if the first argument is 'all' all values default to those specified in config.py
            if option in ['THOST', 'thost']:
                print(f'THOST => {value}')
                self.option_list[0] = value

            elif option in ['TPORT', 'tport']:
                if '/' in value:
                    self.option_list[1]['value'] = value.split('/')
                    self.option_list[1]['type'] = 'range'
                    display = self.option_list[1]['value']
                    print(f'TPORT => {display}')

                elif ',' in value:
                    self.option_list[1]['value'] = value.split(',')
                    self.option_list[1]['type'] = 'group'
                    display = self.option_list[1]['value']
                    print(f'TPORT => {display}')

                else:
                    self.option_list[1]['value'] = int(value)
                    self.option_list[1]['type'] = 'single'
                    display = self.option_list[1]['value']
                    print(f'TPORT => {display}')

            elif option in ['PROTO', 'proto', 'protocol', "PROTOCOL"]:
                print(f'PROTO => {value}')
                self.option_list[2] = value

            elif option in ['TMOUT', 'tmout']:
                if isFloat(value):
                    print(f'TMOUT => {value}')
                    self.option_list[3] = value
                else:
                    print(f'{_FALERT}Error: Invalid value provided')
                    self.option_list[8]=1

            elif option in ['TRYCT', 'tryct']:
                if value.isdigit():
                    print(f'TRYCT => {value}')
                    self.option_list[4] = int(value)
                else:
                    print(f'{_FALERT}Error: Invalid value provided')
                    self.option_list[8]=1

            elif option in ['NMAP', 'nmap']:
                if value.isdigit():
                    print(f'NMAP  => {value}')
                    self.option_list[5] = int(value)
                else:
                    print(f'{_FALERT}Error: Invalid value provided')
                    self.option_list[8]=1

            elif option in ['VERBOSE', 'verbose']:
                if value not in ['true', 'false']:
                    print(_FALERT+'Error: Invalid value provided')
                    self.option_list[8]=1
                elif value == 'true':
                    self.option_list[6] = True
                    print(f'VERBOSE => {self.option_list[6]}')
                elif value == 'false':
                    self.option_list[6] = False
                    print(f'VERBOSE => {self.option_list[6]}')

            elif option in ['THREADING', 'threading']:
                if value not in ['true', 'True', 'false', 'False']:
                    print(f'{_FALERT}Error: Invalid value provided')
                    self.option_list[8] = 1
                elif value in ['true', 'True']:
                    self.option_list[7] = True
                else:
                    self.option_list[7] = False
                print(f'THREADING => {self.option_list[7]}')

            else:
                print(_FALERT+'[-] Error: Invalid option ', option)
                self.option_list[8] = 1

        elif option == 'all':
            # If there are no values in the config.py then,
            # this is same as `unset all`
            self.option_list[0] = variables.THOST
            self.option_list[1] = variables.tport()
            self.option_list[2] = variables.PROTOCOL
            self.option_list[3] = variables.timeout()
            self.option_list[4] = variables.trycount()
            self.option_list[5] = variables.Nmap()
            self.option_list[6] = variables.Verbose()
            self.option_list[7] = variables.Threading()

        elif not value:
            print(f'{_FALERT}[-] Error: no value provided to option')
            self.option_list[8] = 1

        else:
            print(f"{_FALERT}[-] Error: Invalid value provided to option")
            self.option_list[8] = 1