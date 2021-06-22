#! /usr/bin/env python3

# This is the port prober module which just scans for open ports on a given lhost

import socket

openports = []

# Get the service name based on the port
def __getServbyPort(port, protocol):
    try:
        name = socket.getservbyport(int(port), protocol)
        return name
    except:
        return False

# TCP port scanner function
def __tscanner(host, port, timeout):
    socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Port = int(port)
    TMOUT = int(timeout)
    try:
        socktcp.settimeout(TMOUT)
        socktcp.connect((host, Port))
        return True

    except Exception as exp:
        print(exp)
        return False

    finally:
        socktcp.close()

# UDP port scanner function
def __uscanner(host, port, timeout, tryct):
    Port = int(port)
    TMOUT = int(timeout)
    portstatus = False
    sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sockicmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    for _ in range(tryct):
        try:
            sockudp.sendto(bytes('', 'utf-8'), (host, Port))
            sockicmp.settimeout(TMOUT)
            data, addr = sockicmp.recvfrom(1024)

        except socket.timeout:
            serv = __getServbyPort(Port, 'udp')
        
            if not serv:
                portstatus = False
            else:
                portstatus = True

        except socket.error as e:
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
def scanner(host, port, timeout, protocol, tryct):
    if protocol in ['tcp', 'tcp/ip', 'TCP', 'TCP/IP']:
        if __portinputislist(port):
            for x in range((int(str(port[0]))), (int(str(port[1]))+1)):
                if __tscanner(host, int(x), timeout):
                    opeStr = f"{host}: {x} is open"
                    openports.append(opeStr)
                    print(opeStr)

                else:
                    print(f"{host}: {x} is closed")

            print("-"*60)

            for x in openports:
                print(x)

            openports.clear()


        else:
            if __tscanner(host, port, timeout):
                print(f"{host}: {port} is open")

            else:
                print(f"{host}: {port} is closed")

    elif protocol in ['udp', 'UDP']:
        if __portinputislist(port):
            for x in range((int(str(port[0]))), (int(str(port[1]))+1)):
                if __uscanner(host, x, timeout, tryct):
                    opeStr = f"{host}: {x} is open"
                    openports.append(opeStr)
                    print(opeStr)

                else:
                    print(f"{host}: {x} is closed")

            print("-"*60)

            for x in openports:
                print(x)

            openports.clear()


        else:
            if __uscanner(host, port, timeout, tryct):
                print(f"{host}: {port} is open")

            else:
                print(f"{host}: {port} is closed")

    else:
        raise Exception('Error: Unknown protocol specified')
