# Installation of Scapy

# *** This installed Scapy a tool, not the Python library ***
# Add /home/saiello/.local/bin to the PATH variable 
# Updating the path - https://itsfoss.com/add-directory-to-path-linux/

# *** This installed scapy for Python3 *** 
# sudo apt install python3-scapy

from scapy.all import sniff, IP #, TCP, UDP


def packet_callback(packet):
    if packet[IP].payload:
        print(f'[*] Destination: {packet[IP].src}')
        print(f'[*] Destination: {packet[IP].dst}')


def main():
    sniff(filter='ip and host not 192.168.1.100', prn=packet_callback, store=0)

if __name__ == "__main__":
    main()
