import socket
import os
import sys

HOST = '192.168.1.100'

def main():
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    #? Other sockets like stream sockets and data gram sockets receive data from the transport layer that contains no headers but only the payload. This means that there is no information about the source IP address and MAC address. 
    #* https://www.opensourceforu.com/2015/03/a-guide-to-using-raw-sockets/

    sniffer.bind((HOST, 0))

    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    #? Figure out what IP_HDRINCL does for sure
    #* https://man7.org/linux/man-pages/man7/raw.7.html

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            print(sniffer.recvfrom(65565))

            #? Linux ICMP payload is: (!\”#\$%&\‘()*+,-./01234567)
            #? Windows ICMP payload is: abcdefghijklmnopqrstuvwabcdefghi
            #* http://blog.alan-kelly.ie/blog/payload_comparsion/


    except KeyboardInterrupt:
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()


if __name__ == '__main__':
    main()