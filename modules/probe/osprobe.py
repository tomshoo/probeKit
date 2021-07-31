from scapy.all import *
import nmap
import socket
from config import colors

FRED = colors.FALERT
FWHITE = colors.FNORMAL
FGREEN = colors.FSUCCESS
FYELLOW = colors.FURGENT

def checkTTL(target, iterator):
    pkt = IP(dst=target)/ICMP(seq=9999)
    ttllist = []

    if iterator == 0:
        raise Exception(f'{FRED}Error: invalid try count specified: {iterator}{FWHITE}')

    for _ in range(iterator):
        rpkt = sr1(pkt)
        rpttl = rpkt[IP].ttl
        ttllist.append(rpttl)

    return ttllist

class checkOS():
    nmapscanner = nmap.PortScanner()
    def __init__(self, target, iterator, ifnmap):
        self.target = target
        self.iterator = iterator
        self.ifnmap = ifnmap

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
            print(FRED+"Error: Unable to identify OS via Nmap")
        else:
            for data in OSresult['osmatch']:
                for i in data:
                    print(data[i])

    def scanner(self):
        print("Running TTL check on host")
        print("Please wait...")

        HostOSbyTTL = self.OSbyTTL()
        print(f"{FGREEN}[*] Host appears to be running {HostOSbyTTL} based OS{FWHITE}")

        if self.ifnmap == 1:
            print("Please wait running Nmap scan...")
            self.nmapScan()

        elif self.ifnmap == 0:
            print(f'{FYELLOW}Alert: Skipping nmap scan')

        else:
            raise Exception(f'{FRED}Error: invalid condition for nmap: {self.ifnmap}{FWHITE}')
