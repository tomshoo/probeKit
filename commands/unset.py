from config import colors as _colors

_FALERT = _colors.FALERT

class unset_val:
    def __init__(self, option_list: list, options: str):
        ret_list: list = [option_list, 0]
        self.ret_list = ret_list
        self.options = options
        
    def run(self):
        for option in self.options:
            self.unassign(option)
        return self.ret_list

    def unassign(self, option):
        option_list = self.ret_list[0]
        exit_code = self.ret_list[1]
        """Function to unassign values from an asked option."""
        if option in ['THOST', 'thost']:
            print(f'{_FALERT}unset THOST')
            option_list[0] = ''

        elif option in ['TPORT', 'tport']:
            print(f'{_FALERT}unset TPORT')
            option_list[1]['value'] = ''
            option_list[1]['type'] = ''

        elif option in ['PROTO', 'proto', 'protocol', 'PROTOCOL']:
            print(f'{_FALERT}unset PROTO')
            option_list[2] = ''

        elif option in ['TMOUT', 'tmout']:
            print(f'{_FALERT}unset TMOUT')
            option_list[3] = 1

        elif option in ['TRYCT', 'tryct']:
            print(f'{_FALERT}unset TRYCT')
            option_list[4] = 1

        elif option in ['NMAP', 'nmap']:
            print(f'{_FALERT}unset NMAP')
            option_list[5] = 0

        elif option in ['VERBOSE', 'verbose']:
            print(f'{_FALERT}unset VERBOSE')
            option_list[6] = ''

        elif option in ['THREADING', 'threading']:
            print(f'{_FALERT}unset THREADING')
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
            print(_FALERT+'Error: Invalid option')
            exit_code = 1
            
        self.ret_list[0] = option_list
        self.ret_list[1] = exit_code