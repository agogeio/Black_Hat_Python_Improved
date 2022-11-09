# Packet sniffer in python for Linux
# Sniffs only incoming TCP packet
# Origional credit https://www.binarytides.com/python-packet-sniffer-code-linux/

import socket, sys
from struct import *

def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(chr(a[0])) , ord(chr(a[1])) , ord(chr(a[2])), ord(chr(a[3])), ord(chr(a[4])) , ord(chr(a[5])))
  return b

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
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
    print ('Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol))



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
        
        print ('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr))