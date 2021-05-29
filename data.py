from colorama import Fore, Back
# Foreground colors

class colors():
    FALERT   = Fore.RED
    FSUCCESS = Fore.GREEN
    FNORMAL  = Fore.WHITE
    FURGENT  = Fore.YELLOW
    FPROMPT    = Fore.BLUE

    # Background colors (still do not have any use)

    BALERT = Back.RED
    BSUCCESS = Back.GREEN
    BNORMAL = Back.BLACK
    BURGENT = Back.YELLOW

class variables():
    LHOST = ''
    LPORT = ''
    PROTOCOL = ''
    TIMEOUT = '1'
    TRYCT = 1
    NMAP = 0
