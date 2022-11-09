# Packet sniffer in python for Linux
# Sniffs only incoming TCP packet
# Origional credit https://www.binarytides.com/python-packet-sniffer-code-linux/

import socket, sys
from struct import *

def eth_addr (a) :
		b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(chr(a[0])) , ord(chr(a[1])) , ord(chr(a[2])), ord(chr(a[3])), ord(chr(a[4])) , ord(chr(a[5])))
		return b

try:
	s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
except socket.error as msg:
	print ('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

while True:
		packet = s.recvfrom(65565)
		packet = packet[0]
		#parse ethernet header
		eth_length = 14

		eth_header = packet[:eth_length]
		eth = unpack('!6s6sH' , eth_header)
		eth_protocol = socket.ntohs(eth[2])
		print (f'Destination MAC:\t{eth_addr(packet[0:6])}\tSource MAC:\t{eth_addr(packet[6:12])}\tProtocol: {str(eth_protocol)}')

		#Parse IP packets, IP Protocol number = 8
		if eth_protocol == 8 :
				#Parse IP header
				#take first 20 characters for the ip header
				ip_header = packet[eth_length:20+eth_length]
				ip_header = unpack('!BBHHHBBH4s4s' , ip_header)
				version_ihl = ip_header[0]
				version = version_ihl >> 4
				ihl = version_ihl & 0xF
				iph_length = ihl * 4
				ttl = ip_header[5]
				protocol = ip_header[6]

				s_addr = socket.inet_ntoa(ip_header[8]);
				d_addr = socket.inet_ntoa(ip_header[9]);
				
				print (f'Destination Address:\t{str(d_addr)}\t\tSource Address:\t{str(s_addr)}\t\tProtocol: {str(protocol)}\tVersion: {str(version)}\tIP Header Length: {str(ihl)}\tTTL: {str(ttl)}\t')


		#TCP protocol
		if protocol == 6 :
			t = iph_length + eth_length
			tcp_header = packet[t:t+20]

			#now unpack them :)
			tcph = unpack('!HHLLBBHHH' , tcp_header)
			
			source_port = tcph[0]
			dest_port = tcph[1]
			sequence = tcph[2]
			acknowledgement = tcph[3]
			doff_reserved = tcph[4]
			tcph_length = doff_reserved >> 4
			
			print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
			
			h_size = eth_length + iph_length + tcph_length * 4
			data_size = len(packet) - h_size
			
			#get data from the packet
			data = packet[h_size:]
			
			print 'Data : ' + data