from colorama import Fore, Back

# configure colors in this class
class colors():
    FALERT   : str = Fore.RED
    FSUCCESS : str = Fore.GREEN
    FNORMAL  : str = Fore.WHITE
    FURGENT  : str = Fore.YELLOW
    FPROMPT  : str = Fore.BLUE

    # Background colors (still do not have any use)

    BALERT   : str = Back.RED
    BSUCCESS : str = Back.GREEN
    BNORMAL  : str = Back.BLACK
    BURGENT  : str = Back.YELLOW

# provide defaults for all the options for a module
# These values will be overridden if user tends to unset the value
class variables():
    MODULE   : str = ''
    LHOST    : str = ''
    LPORT          = ''
    PROTOCOL : str = ''
    TIMEOUT  : int = 1
    TRYCT    : int = 1
    NMAP     : int = 0
    VERBOSE  : str = ''

# Aliases for the user's comfort
aliases : dict = {
    'exec': 'run',
    'execute': 'run',
    'c': 'clear',
    'probe': 'use probe',
    'info': 'show info',
    'options': 'show options',
    'getstatus': 'show status'
}
