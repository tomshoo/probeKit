# This is the port prober module which just scans for open ports on a given thost


# Imports
import socket
import concurrent.futures
from config import colors
from modules.utils import datevalue, timestamp

# Additional colors
BALERT = colors.BALERT
FSUCCESS = colors.FSUCCESS
FNORMAL = colors.FNORMAL
BURGENT = colors.BURGENT
FALERT = colors.FALERT
BNORMAL = colors.BNORMAL

# Lists for presenting output
results: list = []
openports: list = []

# List of valid protocols to be used with this module
valid_protocols: list = ['tcp', 'tcp/ip', 'TCP', 'TCP/IP', 'udp', 'UDP']

# Get the service name based on the port
def __getServbyPort(port, protocol):
    try:
        name = socket.getservbyport(int(port), protocol)
        return name
    except:
        return False

# TCP port scanner function
def __tscanner(host, port, timeout, verbose):
    socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TMOUT = int(timeout)
    try:
        socktcp.settimeout(TMOUT)
        socktcp.connect((host, port))
        return True

    except Exception as exp:
        if verbose:
            print(FALERT, port, exp, FNORMAL)
        return False

    finally:
        socktcp.close()

# UDP port scanner function
def __uscanner(host, port, timeout, tryct, verbose):
    TMOUT = int(timeout)
    portstatus = False
    sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sockicmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    for _ in range(tryct):
        try:
            sockudp.sendto(bytes('This is a test', 'utf-8'), (host, port))
            sockicmp.settimeout(TMOUT)
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

# Checks if the given port input was in form of list or string
# if port input is list the first element will be first port and the second element will be the last port
def __portinputislist(port):
    if 'list' in str(type(port)):
        return True

    elif 'str' in str(type(port)):
        return False

    else:
        exception = TypeError(f'{FALERT}[*] Error: Unknown input type{FNORMAL}')
        return exception

# Starts the actual scanner session
def scanner(host, port, timeout, protocol, tryct, verbose=False):
    if protocol in ['tcp', 'tcp/ip', 'TCP', 'TCP/IP']:
        if __tscanner(host, port, timeout, verbose):
            serv = __getServbyPort(port, 'tcp')
            return f'{FSUCCESS}[+] {protocol}: {host}: {port} is open, service: {serv}{FNORMAL}'
        else:
            return f'{FALERT}[-] {protocol}: {host}: {port} is closed{FNORMAL}'

    elif protocol in ['udp', 'UDP']:
        if __uscanner(host, port, timeout, tryct, verbose):
            serv = __getServbyPort(port, 'udp')
            return f'{FSUCCESS}[+] {protocol}: {host}: {port} is open, service: {serv}{FNORMAL}'
        else:
            return f'{FALERT}[-] {protocol}: {host}: {port} is closed{FNORMAL}'

# Displays the output
# Also provides multithreading it the port input is a list
def display(host, port, timeout, protocol, tryct, verbose, threading):
    # Check if the specified protocol is valid
    if protocol in valid_protocols:
        executor = concurrent.futures.ThreadPoolExecutor()
        # check if input is a single port or a range
        print(f'{BURGENT}[**] Scan started at {datevalue()}{BNORMAL}')
        start = timestamp()
        if __portinputislist(port):
            try:
                p_begin: int = int(port[0])
                p_end: int = int(port[1])+1

                # Initiate multi-threaded process
                if threading:
                    output = [ executor.submit(scanner, host, x, timeout, protocol, tryct, verbose) for x in range(p_begin, p_end) ]
                    for f in concurrent.futures.as_completed(output):
                        # Prevents unnecessary output if verbose is set to false
                        if f.result():
                            results.append(f.result())
                else:
                    output = [ scanner(host, x, timeout, protocol, tryct, verbose) for x in range(p_begin, p_end) ]
                    for x in output:
                        if x:
                            results.append(x)
                # Finally print the value on the basis of what value was set to verbose
                if verbose:
                    for x in results:
                        if 'open' in x:
                            openports.append(x)
                        print(x)

                    print('-'*60)
                    for y in openports:
                        print(y)

                else:
                    for x in results:
                        if 'open' in x:
                            print(x)
                        else:
                            print(x, end='\r')
                end = timestamp()

                print(f'{BURGENT}[**] Scan took about {round(end-start, 5)} sec(s).{BNORMAL}')

            except KeyboardInterrupt:
                print(f'{FALERT}Keyboard interrupt received, quitting!!')
                if threading:
                    executor.shutdown(wait=False, cancel_futures=True)

            results.clear()

        else:
            portstatus = scanner(host, int(port), timeout, protocol, tryct, verbose)
            print(portstatus)
            if portstatus:
                print(portstatus)
            else:
                print(f'{protocol}: {host}: {port} is closed')

    else:
        print(f'{BALERT}[-] Error: Unknown protocol specified{BNORMAL}')