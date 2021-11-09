from config import colors
from rich import traceback, console

traceback.install()

FALERT = colors.FALERT
FURGENT = colors.FURGENT
FSUCCESS = colors.FSUCCESS

Console = console.Console()

class Info():
    """List available options for a selected module"""
    def __init__(self, MODULE: str):
        self.module = MODULE

    def showInfo(self):
        """Display the options for available modules."""
        module: str = self.module

        if module == 'probe':
            Console.print(f'\n\t[*] THOST => hosts ip4 address (required) (THOST => thost)\n'
            f'\t[*] TPORT => ports to scan on host (required) (TPORT => tport)\n'
            f'[{FALERT}]\t             | values can be set as:[/]\n'
            f'\t                                   | \[portnumber] (single port scan)\n'
            f'\t                                   | \[startport/endport] (port range)\n'
            f'\t                                   | \[port1,port2,port3,...] (port group)\n\n'
            f'\t[*] PROTO => protocol to use for scanning (required) (PROTO => proto)\n'
            f'\t[{FALERT}]             | Available protocols:[/] \n'
            f'\t                                  | [TCP => tcp => TCP/IP => tcp/ip]\n'
            f'\t                                  | [UDP => udp]\n\n'
            f'\t[*] TMOUT => time to wait for incomming packet in seconds (set to \'1\' by default)(TMOUT => tmout)\n\n'
            f'\t[*] TRYCT => number of tries to perform while performing UDP scan (set to \'1\' by default)(TRYCT => tryct)\n\n'
            f'\t[*] VERBOSE => Provide a verbose output or not (VERBOSE => verbose)\n'
            f'\t[{FALERT}]                     | Available options are true (or) false\n\n[/]'
            f'\t[*] THREADING => Allow threading while scanning ports (THREADING => threading)\n'
            f'\t[{FALERT}]                     | Available options are true (or) false\n[/]')
            return 0

        elif module == 'osprobe':
            Console.print(f'\n\t[*] THOST => hosts ip4 address (required) (THOST => thost)\n\n'
            f'\t[*] TRYCT => number of tries to send the packet (set to \'1\' by default) (TRYC => tryc)\n\n'
            f'\t[*] NMAP  => should we perform an NMAP scan? (set to \'0\' by default) (NMAP => nmap)\n'
            f'\t[{FALERT}]           | 0 implies flase\n'
            f'\t           | 1 implies true\n'
            f'\t           | WARNING: Use at your own risk\n[/]')
            return 0

        elif module == 'dirfuzz':
            Console.print('\n\t[white]TURL     => Complete url of the target `http(s)://<domain name>/`\n'
            '\tMODE     => Type of brute forcing\n'
            '\t\t | subdomain: bruteforce the subdomain for the given url\n'
            '\t\t | directory: bruteforcing the directories in the given url\n'
            '\tWORDLIST => Path to a wordlist file\n'
            '\t\t | Path can be relative\n'
            '\t\t | Use proper structure for your operating system\n'
            '\t\t\t - `/` for *nix and `\\` for dos based systems\n'
            '\tDEPTH    => Depth to crawl if type is set to `directory`\n'
            '\tVERBOSE  => Display an expanded output if set to true[/]\n')
            return 0

        elif not module:
            Console.print(f'[{FALERT}]Error: No module selected[/]')
            return 2
        else:
            Console.print(f'[{FALERT}]Error: Invalid module[/]')
            return 1