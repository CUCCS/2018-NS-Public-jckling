#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scapy.all import *

# TCP flags
# 'F': 'FIN', FIN = 0x01
# 'S': 'SYN', SYN = 0x02
# 'R': 'RST', RST = 0x04
# 'P': 'PSH', PSH = 0x08
# 'A': 'ACK', ACK = 0x10
# 'U': 'URG', URG = 0x20
# 'E': 'ECE', ECE = 0x40
# 'C': 'CWR', CWR = 0x80

def udp_scan(ip, port, timeout=3):
	pkt = IP(dst=ip)/UDP(dport=port)
	res = sr1(pkt, timeout=timeout, verbose=False)
	if str(type(res)) != "<type 'NoneType'>":
		if res.haslayer(UDP):
			return 'open'
		elif res.haslayer(ICMP):
			if res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code == 3:
				return 'closed'
			elif res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code in [1, 2, 9, 10, 13]:
				return 'filtered'

def tcp_connect_scan(ip, port, timeout=3):
	pkt = IP(dst=ip)/TCP(dport=port, flags='S')
	res = sr1(pkt, timeout=timeout, verbose=False)
	if str(type(res)) == "<type 'NoneType'>":
		return 'closed'
	elif res.haslayer(TCP):
		if res.getlayer(TCP).flags == 'AS':
			res1 = sr1(IP(dst=ip)/TCP(dport=port, flags='A'), timeout=timeout, verbose=False)
			return 'open'
		elif res.getlayer(TCP).flags == 'AR':
			return 'closed'

def tcp_stealth_scan(ip, port, timeout=3):
	pkt = IP(dst=ip)/TCP(dport=port, flags='S')
	res = sr1(pkt, timeout=timeout, verbose=False)
	if str(type(res)) == "<type 'NoneType'>":
		return 'filtered'
	elif res.haslayer(TCP):
		if res.getlayer(TCP).flags == 'AS':
			res1 = sr1(IP(dst=ip)/TCP(dport=port, flags='R'), timeout=timeout, verbose=False)
			return 'open'
		elif res.getlayer(TCP).flags == 'AR':
			return 'closed'
		elif res.haslayer(ICMP) and res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]:
			return 'filtered'

def tcp_xmas_null_fin_scan(ip, port, typ='xmas', timeout=3):
	if typ.lower() == 'xmas':
		pkt = IP(dst=ip)/TCP(dport=port, flags='FPU')
	elif typ.lower() == 'null':
		pkt = IP(dst=ip)/TCP(dport=port, flags='')
	elif typ.lower() == 'fin':
		pkt = IP(dst=ip)/TCP(dport=port, flags='F')
	res = sr1(pkt, timeout=timeout, verbose=False)
	if str(type(res)) == "<type 'NoneType'>":
		return 'open|filtered'
	elif res.haslayer(TCP):
		if res.getlayer(TCP).flags == 'AR':
			return 'closed'
	elif res.haslayer(ICMP):
		if res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]:
			return 'filtered'

def tcp_ack_scan(ip, port, timeout=3):
	pkt = IP(dst=ip)/TCP(dport=port, flags='A')
	res = sr1(pkt, timeout=timeout, verbose=False)
	if str(type(res)) == "<type 'NoneType'>":
		return 'Stateful firewall presentn(Filtered)'
	elif res.haslayer(TCP):
		if res.getlayer(TCP).flags == 'R':
			return 'No firewalln(Unfiltered)'
	elif res.haslayer(ICMP):
		if res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]:
			return 'Stateful firewall presentn(Filtered)'

def result(ip, port=0, timeout=3, pro='udp', typ=''):
	a, b = pro.lower(), typ.lower()
	f = {'connect':'S', 'stealth':'S', 'xmas':'FPU', 'null':'', 'fin':'F', 'ack':'A'}
	if a == 'udp':
		pkt = IP(dst=ip)/UDP(dport=port)
	elif a == 'tcp':
		if b in f.keys():
			pkt = IP(dst=ip)/TCP(dport=port, flags=f[typ])
		else:
			return null
	r = sr1(pkt, timeout=timeout, verbose=False)
	if a == 'udp':
		if r:
			if r.haslayer(UDP):
				table = ['open', 'listen']
			if r.haslayer(ICMP) and r.getlayer(ICMP).type == 3:
				table = ['closed', 'filtered']
		else:
			table = ['closed', 'filtered']
	elif a == 'tcp':
		if b=='connect' or b=='stealth':
			if r:
				if r.haslayer(TCP) and r.getlayer(TCP).flags == 'SA':
					if b == 'connect':
						res1 = sr(IP(dst=ip)/TCP(dport=r.getlayer(TCP).dport,flags='AR'), timeout=timeout, verbose=False)
						table = ['listen']
					else:
						res1 = sr(IP(dst=ip)/TCP(dport=r.getlayer(TCP).dport,flags='R'), timeout=timeout, verbose=False)
						table = ['open', 'listen']
				if r.haslayer(TCP) and r.getlayer(TCP).flags == 'AR':
					table = ['closed']
				if r.haslayer(ICMP) and r.getlayer(ICMP).type == 3:
					table = ['filtered']
			else:
				table = ['filtered']
		elif b=='xmas' or b=='null' or b=='fin':
			if r:
				if r.haslayer(TCP) and r.getlayer(TCP).flags == 'AR':
					table = ['closed']
				if r.haslayer(ICMP) and r.getlayer(ICMP).type == 3:
					table = ['open', 'listen', 'filtered']
			else:
				table = ['open', 'listen', 'filtered']
		elif b=='ack':
			if r:
				if r.haslayer(TCP) and r.getlayer(TCP).flags == 'R':
					table = ['filtered']
				if r.haslayer(ICMP) and r.getlayer(ICMP).type == 3:
					table = ['closed']
			else:
				table = ['closed']
	return table

if __name__ == '__main__':
	ip = '192.168.56.101'
	port = 80
	types = ['connect', 'stealth', 'xmas', 'null', 'fin', 'ack']

	print 'UDP SCAN'
	print(result(ip, port=port))
	print('')

	for t in types:
		print 'TCP', t, 'SCAN'
		print result(ip, port=port, pro='tcp',typ=t)
		print('')
	
	# print udp_scan(ip, port)
	# print tcp_connect_scan(ip, port)
	# print tcp_stealth_scan(ip, port)
	# print tcp_xmas_null_fin_scan(ip, port, typ='xmas')
	# print tcp_xmas_null_fin_scan(ip, port, typ='null')
	# print tcp_xmas_null_fin_scan(ip, port, typ='fin')
	# print tcp_ack_scan(ip, port)	