import argparse
from scapy.all import *

parser = argparse.ArgumentParser()
parser.add_argument('address', help='Hostname')
args=parser.parse_args()

target=args.address

pkt  = IP(dst=target)/TCP(flags='S', dport=443)
isn = pkt.seq
rpkt = sr1(pkt)

sequence = isn + 1
payload='ACK'
acknowledge=rpkt[TCP].ack

#opkt=send(IP(dst=target)/TCP(flags='A', dport=443, ack=acknowledge, seq=sequence))