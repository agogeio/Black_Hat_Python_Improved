# Installation of Scapy

# *** This installed Scapy a tool, not the Python library ***
# Add /home/saiello/.local/bin to the PATH variable 
# Updating the path - https://itsfoss.com/add-directory-to-path-linux/

# *** This installed scapy for Python3 *** 
# sudo apt install python3-scapy

# *** Ubuntu Connectivity Check *** 
# https://ubuntu.com/core/docs/networkmanager/snap-configuration/connectivity-check

from scapy.all import sniff, TCP, IP, UDP

def packet_callback(packet):
    if packet[TCP].payload:
        print(f'[*] Source: {packet[IP].src}')
        print(f'[*] Destination: {packet[IP].dst}')
        print(f'[*] Payload: {packet[TCP].payload}')
    elif packet[UDP].payload:
        print(f'[*] Source: {packet[IP].src}')
        print(f'[*] Destination: {packet[IP].dst}')
        print(f'[*] Payload: {packet[UDP].payload}')


def main():
    sniff(filter='tcp port 80 or tcp port 443 or udp port 53',prn=packet_callback, count=0)
    #sniff(filter='udp port 53',prn=packet_callback, count=0)


if __name__ == "__main__":
    main()
