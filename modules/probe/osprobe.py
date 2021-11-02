"""
OS-prober module using scapy and python-nmap.

- check for the TTL in the ICMP ping response,
- check the os via an nmap scan if nmap is enabled.
"""

# Imports
from scapy.all import IP,ICMP,sr1
import nmap
import socket
from config import colors as colors
from rich.console import Console as Con

Console = Con()

FALERT = colors.FALERT
FSUCCESS = colors.FSUCCESS
FURGENT = colors.FURGENT

def checkTTL(target, iterator):
    """
    Function to check the TTL value in an ICMP ping response.
    """
    pkt = IP(dst=target)/ICMP(seq=9999)
    ttllist = []

    if iterator == 0:
        Console.print(f'[{FALERT}]Error: invalid try count specified: {iterator}[/]')

    for _ in range(iterator):
        rpkt = sr1(pkt)
        rpttl = rpkt[IP].ttl
        ttllist.append(rpttl)

    return ttllist

class checkOS():
    """
    Driver class where the output of checkTTL will be processed along with the nmap(if enabled) result.
    """
    nmapscanner = nmap.PortScanner()
    def __init__(self, target, iterator, ifnmap):
        self.target = target
        self.iterator = iterator if iterator else 1
        self.ifnmap = ifnmap if ifnmap else 0

    def OSbyTTL(self):
        ttllist = checkTTL(self.target, self.iterator)
        for i in ttllist:
            if i <= 64:
                return "Linux"

            elif i <= 128:
                return "DOS"

            elif i <= 256:
                return "Solaris"

    def nmapScan(self):
        scanner = self.nmapscanner
        target = self.target
        targetip = socket.gethostbyname(target)

        OSresult = scanner.scan(hosts=target, arguments="-O")['scan'][targetip]
        if not OSresult['osmatch']:
            Console.print(f"[{FALERT}]Error: Unable to identify OS via Nmap[/]")
        else:
            for data in OSresult['osmatch']:
                for i in data:
                    print(data[i])

    def scanner(self):
        """
        Take the values and provide the processed output.
        """
        print("Running TTL check on host")
        print("Please wait...")

        HostOSbyTTL = self.OSbyTTL()
        Console.print(f"[{FSUCCESS}][*] Host appears to be running {HostOSbyTTL} based OS[/]")

        if self.ifnmap == 1:
            print("Please wait running Nmap scan...")
            self.nmapScan()

        elif self.ifnmap == 0:
            Console.print(f'[{FURGENT}]Alert: Skipping nmap scan[/]')

        else:
            Console.print(f'[{FALERT}]Error: invalid condition for nmap: {self.ifnmap}[/]')