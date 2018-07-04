from scapy.all import *


def pkt_callback(pkt):
    pkt.show()


sniff(iface="wlp19s0", prn=pkt_callback, filter="tcp", store=0)
