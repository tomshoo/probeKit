from scapy.all import *

def __getTTL(target, iterator):
	pkt = IP(dst=target)/ICMP(seq=9999)
	pktlist = []

	for _ in range(0, iterator):
		rpkt = sr1(pkt)
		if rpkt:
			pktlist.append(rpkt.ttl)

	return pktlist

def checkOS(target, iterator):
	ttllist = __getTTL(target, iterator)
	def checkTTL(ttllist):
		for x in ttllist:
			print(f'observed TTL: {x}')
			if x < 64:
				return 'Linux'

			elif x < 128:
				return 'DOS'

			elif x < 256:
				return 'Solaris'

	if checkTTL(ttllist) == 'Linux':
		print(f'Host possibly running Linux based OS')

	elif checkTTL(ttllist) == 'DOS':
		print(f'Host possibly running Windows or other DOS based OS')

	elif checkTTL(ttllist) == 'Solaris':
		print(f'Host possibly running Solaris based OS')
