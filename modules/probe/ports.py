# This is the port prober module which just scans for open ports on a given lhost

import socket
from threading import Thread
import threading

thread_pool: list = []
openports: list = []

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
            print(exp)
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
                portstatus = False
            else:
                portstatus = True

        except socket.error as e:
            if verbose:
                print(e)

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
        exception = Exception('Error: Unknown input type')
        return exception

# Starts the actual scanner session
def scanner(host, port, timeout, protocol, tryct, verbose=False):
    if protocol in ['tcp', 'tcp/ip', 'TCP', 'TCP/IP']:
        if __tscanner(host, port, timeout, verbose):
            serv = __getServbyPort(port, 'tcp')
            print(f'{protocol}: {host}: {port} is open, service: {serv}')
        elif verbose:
            print(f'{protocol}: {host}: {port} is closed')

    elif protocol in ['udp', 'UDP']:
        if __uscanner(host, port, timeout, tryct, verbose):
            serv = __getServbyPort(port, 'udp')
            print(f'{protocol}: {host}: {port} is open, service: {serv}')
        elif verbose:
            print(f'{protocol}: {host}: {port} is closed')

def display(host, port, timeout, protocol, tryct, verbose):
    if __portinputislist(port):
        for x in range((int(str(port[0]))), (int(str(port[1]))+1)):
            t = Thread(target=scanner, args=(host, x, timeout, protocol, tryct, verbose))
            t.start()
            thread_pool.append(t)

    else:
        scanner(host, port, timeout, protocol, tryct, verbose)

    if len(thread_pool) != 0:
        for threads in thread_pool:
            threads.join()