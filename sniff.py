import pyshark
import socket

# Protocol name from id
table = {num: name[8:] for name, num in vars(socket).items() if name.startswith("IPPROTO")}

capture = pyshark.LiveCapture(interface='wlp19s0')


def print_callback(pkt):
    if 'IP' in pkt:
        src, dst, proto, sport, dport = pkt['ip'].src, pkt['ip'].dst, table[int(pkt['ip'].proto)].lower(), None, None
        if proto in pkt:
            sport, dport = pkt[proto].get('srcport', ''), pkt[proto].get('dstport', '')
        print('{} -- {}:{} -> {}:{}'.format(proto, src, sport, dst, dport))


try:
    capture.apply_on_packets(print_callback, 5)  # sniff 5 seconds
except:
    print("Finished")
