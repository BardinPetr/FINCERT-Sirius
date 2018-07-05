"""
This code was verified on Ubuntu 17.10, Windows 10(English), Mac OSX
"""

from scapy.all import *


def pkt_callback(pkt):
    pkt.show()


# В iface указывать имя своего WI-FI модуля.
sniff(iface="en0", prn=pkt_callback, filter="tcp", store=0)

# sniff(prn=pkt_callback, filter="tcp", store=0) # Windows-style
