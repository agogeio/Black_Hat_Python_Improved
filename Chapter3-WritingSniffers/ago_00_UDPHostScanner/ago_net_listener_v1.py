# Packet sniffer in python for Linux
# Sniffs only incoming TCP packet
# Origional credit https://www.binarytides.com/python-packet-sniffer-code-linux/

import ago_hex_filter
import platform
import socket, sys
from struct import *

def eth_addr (a):
		b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(chr(a[0])) , ord(chr(a[1])) , ord(chr(a[2])), ord(chr(a[3])), ord(chr(a[4])) , ord(chr(a[5])))
		return b

try:
	if platform.system() == 'Linux':
		sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
	elif platform.system == "Windows":
		sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
		# print('Windows support coming soon')
		# sys.exit(0)
	
except socket.error as msg:
	print ('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

while True:
		packet = sniffer.recvfrom(65565)
		packet = packet[0]
		#parse ethernet header
		eth_length = 14

		eth_header = packet[:eth_length]
		eth = unpack('!6s6sH' , eth_header)
		eth_protocol = socket.ntohs(eth[2])
		print (f'ETH FRAME:\tSource MAC:\t{eth_addr(packet[6:12])}\tDestination MAC:\t{eth_addr(packet[0:6])}\tProtocol:\t{str(eth_protocol)}')

		# print(eth_protocol)

		#Parse IP packets, IP Protocol number = 8
		if eth_protocol == 8:
			#Parse IP header
			#take first 20 characters for the ip header
			ip_header = packet[eth_length:20+eth_length]
			ip_header = unpack('!BBHHHBBH4s4s' , ip_header)
			version_ihl = ip_header[0]
			version = version_ihl >> 4
			ihl = version_ihl & 0xF
			iph_length = ihl * 4
			ttl = ip_header[5]
			ip_protocol = ip_header[6]

			s_addr = socket.inet_ntoa(ip_header[8]);
			d_addr = socket.inet_ntoa(ip_header[9]);
			
			print (f'IP PACKET:\tSource Address:\t{str(s_addr)}\t\tDestination Address:\t{str(d_addr)}\t\tProtocol:\t{str(ip_protocol)}\t\tVersion:\t\t{str(version)}\t\tIP Header Lth:\t{str(ihl)}\tTTL: {str(ttl)}\t')

			# print(f'IP Protocol {ip_protocol}')

			#TCP protocol
			if ip_protocol == 6:
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
				
				print (f'TCP PACKET:\tSource Port:\t{str(source_port)}\t\t\tDest Port:\t\t{str(dest_port)}\t\t\tSequence Num:\t{str(sequence)}\tAcknowledgement:\t{str(acknowledgement)}\tTCP header Lth:\t{str(tcph_length)}')
				
				h_size = eth_length + iph_length + tcph_length * 4
				data_size = len(packet) - h_size
				
				#get data from the packet
				data = packet[h_size:]

				# hex_data = ago_hex_filter.hex_dump(data)
				
				# print (str(data))

			#ICMP 
			elif ip_protocol == 1 :
				u = iph_length + eth_length
				icmph_length = 4
				icmp_header = packet[u:u+4]

				#now unpack them :)
				icmph = unpack('!BBH' , icmp_header)
				
				icmp_type = icmph[0]
				code = icmph[1]
				checksum = icmph[2]
				
				print (f'ICMP PACKET:\tType:\t\t{str(icmp_type)}\t\t\tCode:\t\t\t{str(code)}\t\t\tChecksum:\t{str(checksum)}')
				
				h_size = eth_length + iph_length + icmph_length
				data_size = len(packet) - h_size
				
				#get data from the packet
				data = packet[h_size:]
				
				hex_data = ago_hex_filter.hex_dump(data)
				print(f'ICMP Data:\n{hex_data[0]}')

			#UDP
			elif ip_protocol == 17 :
				u = iph_length + eth_length
				udph_length = 8
				udp_header = packet[u:u+8]

				#now unpack them :)
				udph = unpack('!HHHH' , udp_header)
				
				source_port = udph[0]
				dest_port = udph[1]
				length = udph[2]
				checksum = udph[3]
				
				print(f'UDP Packet\tSource Port:\t{str(source_port)}\t\t\tDest Port:\t\t{(dest_port)}\t\t\tLength:\t\t{str(length)}\tChecksum:\t{str(checksum)}')
				
				h_size = eth_length + iph_length + udph_length
				data_size = len(packet) - h_size
				
				#get data from the packet
				data = packet[h_size:]

				udp_hex = ago_hex_filter.hex_dump(data)
				print (f'UDP data:\n{udp_hex[0]}')


		

