# This is the port prober module which just scans for open ports on a given thost


# Imports
import socket
import concurrent.futures
from config import colors
from modules.util.utils import datevalue, timestamp

# Additional colors
BALERT:   str = colors.BALERT
FSUCCESS: str = colors.FSUCCESS
FNORMAL:  str = colors.FNORMAL
BURGENT:  str = colors.BURGENT
FALERT:   str = colors.FALERT
BNORMAL:  str = colors.BNORMAL

# Lists for presenting output
results: list = []
openports: list = []

# List of valid protocols to be used with this module
valid_protocols: list = ['tcp', 'tcp/ip', 'TCP', 'TCP/IP', 'udp', 'UDP']

def __getServbyPort(port, protocol):
    """Get the service name based on the port."""

    try:
        name = socket.getservbyport(int(port), protocol)
        return name
    except:
        return False

def __tscanner(host: str, port: int, timeout: float, verbose: bool):
    """TCP port scanner function."""
    timeout = timeout if timeout else 1

    socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socktcp.settimeout(timeout)
        socktcp.connect((host, port))
        return True

    except Exception as exp:
        if verbose:
            print(FALERT, port, exp, FNORMAL)
        return False

    finally:
        socktcp.close()

def __uscanner(host: str, port: int, timeout: float, tryct: str, verbose: bool):
    timeout = timeout if timeout else 1
    tryct = tryct if tryct else 1
    """UDP port scanner function."""
    portstatus = False
    sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sockicmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    for _ in range(tryct):
        try:
            sockudp.sendto(bytes('This is a test', 'utf-8'), (host, port))
            sockicmp.settimeout(timeout)
            sockicmp.recvfrom(1024)

        except socket.timeout:
            serv = __getServbyPort(port, 'udp')

            if not serv:
                if verbose:
                    print(f'{BALERT}[*] Error: Service on port: {port} not found{BNORMAL}')
                portstatus = False
            else:
                portstatus = True

        except socket.error as e:
            portstatus = False

        finally:
            sockudp.close()
            sockicmp.close()

    return portstatus

def __scanner(host, port, timeout, protocol, tryct, verbose=False):
    """Starts the actual scanner session"""

    if protocol in ['tcp', 'tcp/ip', 'TCP', 'TCP/IP']:
        if __tscanner(host, port, float(timeout), verbose):
            if __getServbyPort(port, 'tcp'):
                serv = __getServbyPort(port, 'tcp')
            else:
                serv = 'Unidentified'

            return f'{FSUCCESS}[+] {protocol}: {host}: {port} is open, service: {serv}{FNORMAL}'
        elif verbose:
            return f'{FALERT}[-] {protocol}: {host}: {port} is closed{FNORMAL}'

    elif protocol in ['udp', 'UDP']:
        if __uscanner(host, port, float(timeout), tryct, verbose):
            if __getServbyPort(port, 'udp'):
                serv = __getServbyPort(port, 'tcp')
            else:
                serv = 'Unidentified'

            return f'{FSUCCESS}[+] {protocol}: {host}: {port} is open, service: {serv}{FNORMAL}'
        elif verbose:
            return f'{FALERT}[-] {protocol}: {host}: {port} is closed{FNORMAL}'

def display(host, port, timeout, protocol, tryct, verbose, threading=False):
    """
    Displays the output.
    Also provides multithreading it the port input is a list.
    """

    if protocol in valid_protocols:
        # Check if the specified protocol is valid
        executor = concurrent.futures.ThreadPoolExecutor()
        # check if input is a single port or a range
        type = port['type']
        print(f'{BURGENT}[**] Scan started at {datevalue()}{BNORMAL}')
        start = timestamp()

        if type == 'single':
            single_port: int = port['value']
            portstatus = __scanner(host, single_port, timeout, protocol, tryct)
            if portstatus:
                print(portstatus)
            else:
                print(f'{protocol}: {host}: {single_port} is closed')

        else:
            try:
                if type == 'range':
                    p_begin: int = int(port['value'][0])
                    p_end: int = int(port['value'][1])+1

                if threading:
                    # Initiate multi-threaded process
                    if type == 'range':
                        output = [ executor.submit(__scanner, host, x, timeout, protocol, tryct, verbose) for x in range(p_begin, p_end) ]
                    else:
                        output = [ executor.submit(__scanner, host, x, timeout, protocol, tryct, verbose) for x in port['value'] ]

                    for f in concurrent.futures.as_completed(output):
                        if f.result():
                            # Prevents unnecessary output if verbose is set to false
                            results.append(f.result())
                else:
                    if type == 'range':
                        output = [ __scanner(host, x, timeout, protocol, tryct, verbose) for x in range(p_begin, p_end) ]
                    else:
                        output = [ __scanner(host, int(x), timeout, protocol, tryct, verbose) for x in port['value'] ]

                    for x in output:
                        if x:
                            results.append(x)

                    output.clear()

                if verbose:
                    # Finally print the value on the basis of what value was set to verbose
                    for x in results:
                        if 'open' in x:
                            openports.append(x)
                        print(x)

                    print('-'*60)
                    for y in openports:
                        print(y)

                    results.clear()
                    openports.clear()

                else:
                    for x in results:
                        print(x)
                results.clear()

            except KeyboardInterrupt:
                print(f'{FALERT}Keyboard interrupt received, quitting!!')
                if threading:
                    executor.shutdown(wait=False, cancel_futures=True)

        end = timestamp()            
        print(f'{BURGENT}[**] Scan took about {round(end-start, 5)} sec(s).{BNORMAL}')

    else:
        print(f'{BALERT}[-] Error: Unknown protocol specified{BNORMAL}')
