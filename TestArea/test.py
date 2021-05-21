import argparse
import nmap
import json

scanner = nmap.PortScanner()

parser = argparse.ArgumentParser()
parser.add_argument('address', help='Hostname')
args=parser.parse_args()

target = args.address

OSresult = scanner.scan(hosts=target, arguments="-O")['scan'][target]['osmatch']
print(type(OSresult))
