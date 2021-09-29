from config import colors as _colors

_FALERT = _colors.FALERT

class unset_val:
    def __init__(self, option_list: list, options: str):
        self.option_list = option_list.append(0)
        self.options = options
        
    def run(self):
        for option in self.options:
            self.unassign(option)
        return self.option_list

    def unassign(self, option):
        """Function to unassign values from an asked option."""
        if option in ['THOST', 'thost']:
            print(f'{_FALERT}unset THOST')
            self.option_list[0] = ''

        elif option in ['TPORT', 'tport']:
            print(f'{_FALERT}unset TPORT')
            self.option_list[1]['value'] = ''
            self.option_list[1]['type'] = ''

        elif option in ['PROTO', 'proto', 'protocol', 'PROTOCOL']:
            print(f'{_FALERT}unset PROTO')
            self.option_list[2] = ''

        elif option in ['TMOUT', 'tmout']:
            print(f'{_FALERT}unset TMOUT')
            self.option_list[3] = 1

        elif option in ['TRYCT', 'tryct']:
            print(f'{_FALERT}unset TRYCT')
            self.option_list[4] = 1

        elif option in ['NMAP', 'nmap']:
            print(f'{_FALERT}unset NMAP')
            self.option_list[5] = 0

        elif option in ['VERBOSE', 'verbose']:
            print(f'{_FALERT}unset VERBOSE')
            self.option_list[6] = ''

        elif option in ['THREADING', 'threading']:
            print(f'{_FALERT}unset THREADING')
            self.option_list[7] = ''

        elif option == 'all':
            self.option_list[0] = ''
            self.option_list[1]['value'] = ''
            self.option_list[1]['type'] = ''
            self.option_list[2] = ''
            self.option_list[3] = 1
            self.option_list[4] = 1
            self.option_list[5] = 0
            self.option_list[6] = ''
            self.option_list[7] = ''
    
        else:
            print(_FALERT+'Error: Invalid option')
            self.option_list[8](1)