from scapy.all import *


def pkt_callback(pkt):
    pkt.show()


# В iface указывать имя своего WI-FI модуля.
sniff(iface="en0", prn=pkt_callback, filter="tcp", store=0)
