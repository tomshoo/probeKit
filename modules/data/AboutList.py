from config import colors as colors, valid_modules as _modules
from rich.console import Console as Con

Console = Con()

FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FURGENT = colors.FURGENT

class moduleHelp():
    """Set of functions containing the description of available modules"""
    #A list containing names of available modules

    def __init__(self, MODULE):
        self.module = MODULE

    def aboutModule(self, moduleName):
        """Prints data about a give module will print data without argument if a module is active"""

        if moduleName == 'probe':
            Console.print(f'[{FALERT}]\nName:\t\t{moduleName}\n'
            'Type:\t\tRecon\n'
            'Description:\tThis module is meant to perform a basic port scan on the specidied host.\n[/]')
            Console.print(f'[{FALERT}]Available options:[/]\n\n'
            f'\t[{FSUCCESS}]THOST => IPv4 address or domain name of the target host\n'
            '\t\t | Can be called THOST or thost\n\n'
            '\tTPORT => ports to be scanned\n'
            '\t\t | Can be called TPORT or tport\n'
            '\t\t | Specify single port as `set tport [portnumber]`\n'
            '\t\t | or a group of ports as `set tport [port1],[port2],[port3],[...]`\n'
            '\t\t | or range multiple ports by `set tport [startPort]/[endPort]`\n\n'
            '\tTMOUT => timeout duration while awaiting connection\n'
            '\t\t | Can be called TMOUT or tmout\n'
            '\t\t | Defaults to 1 second duration\n\n'
            '\tPROTOCOL => Protocol to be used to scan\n'
            '\t\t | Can be called PROTO or proto\n'
            '\t\t | Available Protocols are:\n'
            '\t\t                          | TCP => TCP/IP(tcp => tcp/ip)\n'
            '\t\t                          | UDP(udp)\n\n'
            '\tVERBOSE => show complete output\n'
            '\t\t | Available Options are true/false\n\n'
            '\tTHREADING => use threading for port scanning\n'
            '\t\t | Recommended if the port list is huge, to improve performance of scan\n'
            f'\t\t | [{FURGENT}]do not use if the scan is not taking a long time[/]\n'
            f'[{FSUCCESS}]\t\t | Available options are true (or) false[/][/]\n')

        elif moduleName == 'osprobe':
            Console.print(f'[{FALERT}]\nName:\t\t{moduleName}\n'
            'Type:\t\tRecon\n'
            'Description:\tThis module sends a basic ICMP packet to a host to determine its OS\n'
            '            \t| This module does not confirm the OS since it is just using TTL within the ICMP response\n[/]')
            Console.print(f'[{FSUCCESS}]Available options:\n\n'
            '\tTHOST => IPv4 address or domain name of the target host\n'
            '\t\t | Can be called THOST or thost\n\n'
            '\tTRYCT => Number of times ICMP packet must be sent\n'
            '\t\t | Set to 1 packet by default\n'
            '\t\t | Can be called TRYCT ot tryct\n\n'
            '\tNMAP  => Run an nmap scan\n'
            '\t\t | 0 for false\n'
            '\t\t | 1 for true\n'
            f'[{FALERT}]\t\t | Warning: It is an active scanning method hence use it on your own risk[/][/]\n')

        elif moduleName == 'dirfuzz':
            Console.print(f'[{FALERT}]\nName:\t\t{moduleName}\n'
            'Type:\t\tBruteforcing\n'
            'Description:\tThis module is used for directory (or) subdomain bruteforcing[/]\n')
            Console.print(f'[{FSUCCESS}]Available options:\n\n'
            '\tTURL => Complete url of the target `http(s)://<domain name>/`\n'
            '\tMODE => Type of brute forcing\n'
            '\t\t | subdomain: bruteforce the subdomain for the given url\n'
            '\t\t | directory: bruteforcing the directories in the given url\n'
            '\tWORDLIST => Path to a wordlist file\n'
            '\t\t | Path can be relative\n'
            '\t\t | Use proper structure for your operating system\n'
            '\t\t\t - `/` for *nix and `\\` for dos based systems\n'
            '\tDEPTH => Depth to crawl if type is set to `directory`\n'
            '\tVERBOSE => Display an expanded output if set to true[/]\n')

        elif moduleName == '':
            print(FALERT+'[-] Error: no module selected')

        else:
            print(f'{FALERT}[-] Error: Invalid module \'{moduleName}\'')