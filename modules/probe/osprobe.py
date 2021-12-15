"""
OS-prober module using scapy and python-nmap.

- check for the TTL in the ICMP ping response,
- check the os via an nmap scan if nmap is enabled.
"""

# Imports
from scapy.all import IP,ICMP,sr1
import socket
from config import colors as colors
from rich.console import Console as Con
from typing import List, Union
import nmap

Console = Con()

FALERT = colors.FALERT
FSUCCESS = colors.FSUCCESS
FURGENT = colors.FURGENT

def checkTTL(target, iterator) -> list:
    """
    Function to check the TTL value in an ICMP ping response.
    """
    try:
        pkt = IP(dst=target)/ICMP(seq=9999)
        ttllist = []

        if iterator == 0:
            Console.print(f'[{FALERT}]Error: invalid try count specified: {iterator}[/]')

        for _ in range(iterator):
            rpkt = sr1(pkt)
            rpttl = rpkt[IP].ttl
            ttllist.append(rpttl)

        return ttllist

    except TypeError as err:
        print(err)

class checkOS():
    """
    Driver class where the output of checkTTL will be processed along with the nmap(if enabled) result.
    """
    def __init__(self, target, iterator, ifnmap):
        self.target = target
        self.iterator = iterator if iterator else 1
        self.ifnmap = ifnmap if ifnmap else 0

    def OSbyTTL(self) -> List[Union[str, int]]:
        try:
            ttllist = checkTTL(self.target, self.iterator)
            for i in ttllist:
                if i <= 64:
                    return ["Linux", 0]

                elif i <= 128:
                    return ["DOS", 0]

                elif i <= 256:
                    return ["Solaris", 0]

        except TypeError:
            print('Err: Unable to determine remote host Operating System')
            return None, 0


    def nmapScan(self) -> int:
        try:
            scanner = nmap.PortScanner()
            target = self.target
            targetip = socket.gethostbyname(target)

            OSresult = scanner.scan(hosts=target, arguments="-O")['scan'][targetip]
            if not OSresult['osmatch']:
                Console.print(f"[{FALERT}]Error: Unable to identify OS via Nmap[/]")
                return 1
            else:
                for data in OSresult['osmatch']:
                    for i in data:
                        print(data[i])
        except nmap.PortScannerError:
            Console.print(f'[{FALERT}]Err: `nmap` was not installed!!![/]')
            return 2

        return 0

    def scanner(self) -> int:
        """
        Take the values and provide the processed output.
        """
        print("Running TTL check on host")
        print("Please wait...")

        ttlscan_out: list = self.OSbyTTL()
        HostOSbyTTL = ttlscan_out[0]
        exitcode: int = ttlscan_out[1]
        Console.print(f"[{FSUCCESS}][*] Host appears to be running {HostOSbyTTL} based OS[/]") if HostOSbyTTL else print(end='')

        if self.ifnmap == 1:
            print("Please wait running Nmap scan...")
            return self.nmapScan()

        elif self.ifnmap == 0:
            Console.print(f'[{FURGENT}]Alert: Skipping nmap scan[/]')

        else:
            Console.print(f'[{FALERT}]Error: invalid condition for nmap: {self.ifnmap}[/]')
            return 3

        return exitcode