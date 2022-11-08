import ago_Hex_Filter
import ipaddress    # https://docs.python.org/3/library/ipaddress.html
                    # https://docs.python.org/3/howto/ipaddress.html
import os
import socket
import struct
import sys

# HOST = '192.168.1.100' moving this into main
class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff) 
        # B = 1-byte unsigned char
        # H = 2-byte unsigned short
        # 4s = 4-byte string
        # There's nothing in a struct that allows it to get 4-bytes of data (a nibble)

        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address =  ipaddress.ip_address(self.dst)

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print(f'Error {str(e)}, for protocol number {self.protocol_num}')


def sniff(host):
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    #? Other sockets like stream sockets and data gram sockets receive data from the transport layer that contains no headers but only the payload. This means that there is no information about the source IP address and MAC address. 
    #* https://www.opensourceforu.com/2015/03/a-guide-to-using-raw-sockets/

    sniffer.bind((host, 0)) # This should be a host and port number
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    #? Figure out what IP_HDRINCL does for sure
    #* https://man7.org/linux/man-pages/man7/raw.7.html

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            # print(sniffer.recvfrom(65565))

            #? Linux ICMP payload is: (!\”#\$%&\‘()*+,-./01234567)
            #? Windows ICMP payload is: abcdefghijklmnopqrstuvwabcdefghi
            #* http://blog.alan-kelly.ie/blog/payload_comparsion/

            raw_buffer = sniffer.recvfrom(65565)[0]
            print(type(raw_buffer))
            # str_buffer = raw_buffer.decode()
            # print(str_buffer)
            # hex = ago_Hex_Filter.hex_dump(raw_buffer)
            # print(hex)
            ip_header = IP(raw_buffer[0:20])
            print(f'Protocol: {ip_header.protocol}\nsum: {ip_header.sum}\nsrc: {ip_header.src_address}\ndst: {ip_header.dst_address}\nlen: {ip_header.len}')


    except KeyboardInterrupt:
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        # print(sys.argv[0])
        # print(sys.argv[1])
        host = sys.argv[1]
    else:
        host = '192.168.1.100'
    sniff(host)