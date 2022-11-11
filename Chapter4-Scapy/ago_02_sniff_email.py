# Installation of Scapy

# *** This installed Scapy a tool, not the Python library ***
# Add /home/saiello/.local/bin to the PATH variable 
# Updating the path - https://itsfoss.com/add-directory-to-path-linux/

# *** This installed scapy for Python3 *** 
# sudo apt install python3-scapy

from scapy.all import sniff, TCP, IP


def packet_callback(packet):
    if packet[TCP].payload:
        print(f'[*] Destination: {packet[IP].src}')
        print(f'[*] Destination: {packet[IP].dst}')


def main():
    sniff(filter='tcp port 110 or tcp port 25 or tcp port 143',prn=packet_callback, count=10)

if __name__ == "__main__":
    main()
