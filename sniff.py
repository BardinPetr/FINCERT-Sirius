import pyshark
import socket

# Protocol name from id
table = {num: name[8:] for name, num in vars(socket).items() if name.startswith("IPPROTO")}

# В iface указывать имя своего WI-FI модуля.
capture = pyshark.LiveCapture(output_file='pyshark.pcap',
                              interface='en0')


def print_callback(pkt):
    if 'IP' in pkt:
        src, dst, proto, sport, dport = pkt['ip'].src, pkt['ip'].dst, table[
            int(pkt['ip'].proto)].lower(), None, None
        print(src, dst, proto)
        if proto in pkt:
            #     sport, dport = pkt[proto].get('srcport', ''), pkt[proto].get('dstport', '')
            try:
                sport, dport = pkt[proto].srcport, pkt[proto].dstport
            except:
                pass
        # print((pkt[proto]).get("srcport", ""))
        print('{} -- {}:{} -> {}:{}'.format(proto, src, sport, dst, dport))


capture.apply_on_packets(print_callback)
