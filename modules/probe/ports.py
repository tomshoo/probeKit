# This is the port prober module which just scans for open ports on a given thost

# Imports
import socket
import concurrent.futures
from config import colors as colors
from modules.util.utils import datevalue, timestamp
from rich import traceback, progress, console
Console = console.Console()
traceback.install()

# Additional colors
BALERT:   str = colors.BALERT
FSUCCESS: str = colors.FSUCCESS
BURGENT:  str = colors.BURGENT
FALERT:   str = colors.FALERT

# Lists for presenting output
results: list = []
openports: list = []

# List of valid protocols to be used with this module
valid_protocols: list = ['tcp', 'tcp/ip', 'TCP', 'TCP/IP', 'udp', 'UDP']

class portprobe:
    def __init__(
        self,
        thost: str,
        tport: dict,
        timeout: int,
        protocol: str,
        tryct: int,
        verbose: bool,
        threading: bool
    ):
        self.thost = thost
        self.tport = tport
        self.timeout = timeout if timeout else 1
        self.protocol = protocol
        self.tryct = tryct if tryct else 1
        self.verbose = verbose
        self.threading = threading
        pass


    def __getServbyPort(self, port, protocol) -> bool:
        """Get the service name based on the port."""

        try:
            name = socket.getservbyport(int(port), protocol)
            return name
        except: return None

    def __tscanner(self, port: int) -> bool:
        """TCP port scanner function."""
        host = self.thost
        timeout = self.timeout
        verbose = self.verbose

        socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            socktcp.settimeout(timeout)
            socktcp.connect((host, port))
            return True

        except Exception as exp:
            if self.threading: Console.print(f'[{FALERT}][-]'+" "+str(port)+" "+str(exp)+" "*(len(str(exp))*3)+"[/]", end="\r")
            return False

        finally: socktcp.close()

    def __uscanner(self, port: int) -> bool:
        """UDP port scanner function."""
        host = self.thost
        timeout = self.timeout
        tryct = self.tryct
        verbose = self.verbose
        portstatus = False
        sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sockicmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        for _ in range(tryct):
            try:
                sockudp.sendto(bytes('This is a test', 'utf-8'), (host, port))
                sockicmp.settimeout(timeout)
                sockicmp.recvfrom(1024)

            except socket.timeout:
                serv = self.__getServbyPort(port, 'udp')

                if not serv:
                    if verbose: Console.print(f'[{BALERT}]\[*] Error: Service on port: [bold {BALERT}]{port}[/] not found[/]')
                    portstatus = False
                else: portstatus = True

            except socket.error as e: portstatus = False

            finally:
                sockudp.close()
                sockicmp.close()

        return portstatus

    def __scanner(self, port) -> str:
        """Starts the actual scanner session"""

        if self.protocol in ['tcp', 'tcp/ip', 'TCP', 'TCP/IP']:
            if self.__tscanner(port):
                serv = self.__getServbyPort(port, 'tcp') if self.__getServbyPort(port, 'tcp') else 'Undefined'
                return f'[{FSUCCESS}][+] {self.protocol}: {self.thost}: {port} is open, service: {serv}[/]'
            
            elif self.verbose: return f'[{FALERT}][-] {self.protocol}: {self.thost}: {port} is closed'

        elif self.protocol in ['udp', 'UDP']:
            if self.__uscanner(port):
                serv = self.__getServbyPort(port, 'udp') if self.__getServbyPort(port, 'udp') else 'Undefined'
                return f'[{FSUCCESS}][+] {self.protocol}: {self.thost}: {port} is open, service: {serv}[/]'
            
            elif self.verbose: return f'[{FALERT}][-] {self.protocol}: {self.thost}: {port} is closed'

    def display(self) -> int:
        """
        Displays the output.
        Also provides multithreading it the port input is a list.
        """

        if self.protocol in valid_protocols:
            # Check if the specified protocol is valid
            executor = concurrent.futures.ThreadPoolExecutor()
            # check if input is a single port or a range
            type = self.tport['type']
            port = self.tport
            Console.print(f'[{BURGENT}]\[**] Scan started at {datevalue()}[/]')
            start = timestamp()

            if type == 'single':
                single_port: int = self.tport['value']
                portstatus = self.__scanner(single_port)
                if portstatus: print(portstatus)
                else: print(f'{self.protocol}: {self.host}: {single_port} is closed')
                return 0

            else:
                try:
                    if type == 'range':
                        p_begin: int = int(port['value'][0])
                        p_end: int = int(port['value'][1])+1

                    if self.threading:
                        # Initiate multi-threaded process
                        if type == 'range': output = [ executor.submit(self.__scanner, x) for x in range(p_begin, p_end) ]
                        else: output = [ executor.submit(self.__scanner, x) for x in port['value'] ]

                        for f in concurrent.futures.as_completed(output):
                            if f.result():
                                # Prevents unnecessary output if verbose is set to false
                                results.append(f.result())
                    else:
                        if type == 'range': output = [ self.__scanner(x) for x in progress.track(range(p_begin, p_end), description=f"Scanning {self.protocol}") ]
                        else: output = [ self.__scanner(int(x)) for x in progress.track(port['value'], description=f"Scanning {self.protocol}") ]

                        for x in output:
                            if x: results.append(x)

                        output.clear()

                    if self.verbose:
                        # Finally print the value on the basis of what value was set to verbose
                        for x in results:
                            if 'open' in x: openports.append(x)
                            Console.print(x)

                        print('-'*60)
                        for y in openports: Console.print(y)

                        results.clear()
                        openports.clear()

                    else:
                        for x in results: Console.print(x)
                    results.clear()

                except KeyboardInterrupt:
                    Console.print(f'\n[{FALERT}]Keyboard interrupt received, quitting!![/]')
                    if self.threading: executor.shutdown(wait=False, cancel_futures=True)
                    return 130

                except Exception as e:
                    Console.print(f'[{FALERT}]{str(e)}[/]')
                    return 1

            end = timestamp()            
            Console.print(f'[{BURGENT}][**] Scan took about {round(end-start, 5)} sec(s).[/]')
            return 0

        else:
            Console.print(f'[{BALERT}][-] Error: Unknown protocol specified[/]')
            return 3