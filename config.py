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

    # Please configure the values over here
    MODULE   : str = ''
    THOST    : str = ''
    TPORT    : str = ''
    PROTOCOL : str = ''
    TIMEOUT  : str = '1'
    TRYCT    : str = '1'
    NMAP     : str = '0'
    VERBOSE  : str = ''
    THREADING: str = ''

    # This group of funtions will process the value and return it
    # in the required form
    def tport(self):
        Tport = self.TPORT
        if '/' in Tport:
            return Tport.split('/')
        else:
            return Tport

    def timeout(self):
        tmout = self.TIMEOUT
        if tmout != '':
            return int(tmout)
        else: 
            return ''

    def trycount(self):
        tryct = self.TRYCT
        if tryct != '':
            return int(tryct)
        else:
            return ''

    def Nmap(self):
        nmap = self.NMAP
        if nmap != '':
            return int(nmap)
        else:
            return ''

    def Verbose(self):
        verbose = self.VERBOSE
        if verbose in ['true', 'True']:
            return True
        elif verbose in ['false', 'False']:
            return False
        else:
            return ''

    def Threading(self):
        threading = self.THREADING
        if threading in ['true', 'True']:
            return True
        elif threading in ['false', 'False']:
            return False
        else:
            return ''


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