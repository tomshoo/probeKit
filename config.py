from colorama import Fore, Back

# configure colors in this class
class light():
    #Foreground Colors
    FALERT   : str = Fore.RED
    FSUCCESS : str = Fore.GREEN
    FNORMAL  : str = Fore.BLACK
    FURGENT  : str = Fore.YELLOW
    FPROMPT  : str = Fore.BLUE

    #Background Colors
    BALERT   : str = Back.RED
    BSUCCESS : str = Back.GREEN
    BNORMAL  : str = Back.WHITE
    BURGENT  : str = Back.YELLOW


class dark():
    #Foreground Colors
    FALERT   : str = Fore.RED
    FSUCCESS : str = Fore.GREEN
    FNORMAL  : str = Fore.WHITE
    FURGENT  : str = Fore.YELLOW
    FPROMPT  : str = Fore.BLUE

    #Background Colors
    BALERT   : str = Back.RED
    BSUCCESS : str = Back.GREEN
    BNORMAL  : str = Back.BLACK
    BURGENT  : str = Back.YELLOW

# Chose color scheme(light or dark)
colors = dark

class variables():
    """
    Provide defaults for all the options for a module
    These values will be overridden if user tends to unset the value
    """


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
    WORDLIST:  str = ''

    # This group of funtions will process the value and return it
    # in the required form
    def tport(self):
        Tport = self.TPORT
        tdict = {
            'value': '',
            'type': ''
        }
        if '/' in Tport:
            tdict['value'] = Tport.split('/')
            tdict['type'] = 'range'
        elif ',' in Tport:
            tdict['value'] = Tport.split(',')
            tdict['type'] = 'group'

        else:
            tdict['value'] = Tport
            tdict['type'] = 'single'
        
        return tdict

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

OPTIONS : list = [
    variables().THOST
    , variables().tport()
    , variables().PROTOCOL
    , variables().timeout()
    , variables().trycount()
    , variables().Nmap()
    , variables().Verbose()
    , variables().Threading()
    , variables().WORDLIST
]


# Aliases for the user's comfort
aliases : dict = {
    'execute': 'run',
    'info': 'show info',
    'options': 'show options',
}
