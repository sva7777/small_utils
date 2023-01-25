from scapy.all import *
from scapy.layers.inet import Ether, Dot3
from scapy.contrib.lacp import SlowProtocol, LACP
from scapy.layers.l2 import LLC, SNAP, STP

from pprint import pprint

if __name__ == '__main__':
    all_packets = PcapReader("stp_1.pcap").read_all()

    pkt = Ether()/SlowProtocol()/LACP()

    # ToDo: Write code to send packet
    for p in all_packets:
        sendp(p)

