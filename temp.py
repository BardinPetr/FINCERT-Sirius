"""
This code was verified on Ubuntu 17.10, Windows 10(English), Mac OSX
"""

from scapy.all import *
import datetime
from FilePack import Crypt

result = []
"""
    src = 95.142.205.117
    dst = 10.10.200.213

    src = 10.10.200.213
    dst = 95.142.205.117
    
    src = 163.172.173.40
    dst = 10.10.200.213
    
    src = 173.194.222.189
    dst = 10.10.200.213
    
    
    data = {'ip_get': ['95.142.205.117', '10.10.200.213', '163.172.173.40', '173.194.222.189'], 'ip_post': ['10.10.200.213', '95.142.205.117', '10.10.200.213', '10.10.200.213']}
"""


# def pkt_callback(pkt, data):
#     pkt.show()
# for pack in pkt:
#
#     ip_source = pack[IP].src
#     ip_destination = pack[IP].dst
#
#     tm = pack[IP].time
#     value = datetime.datetime.fromtimestamp(tm)
#     tm = value.strftime('%Y-%m-%d %H:%M:%S')
#
#     if ip_source in data['ip_get']:
#         result.append({'ip': ip_source, 'time': tm, 'type': 'GET'})
#
#     if ip_destination in data['ip_post']:
#         result.append({'ip': ip_destination, 'time': tm, 'type': 'POST'})


# В iface указывать имя своего WI-FI модуля.
# sniff(iface="en0", prn=pkt_callback, filter="tcp", store=0)


# sniff(prn=pkt_callback, filter="tcp", store=0) # Windows-style
# data = {'ip_get': []}
# sniff(prn=lambda x: pkt_callback(x, data), store=0)
# print(result)

# def file_get_contents(filename):
#     with open(filename, 'rb') as f:
#         return f.read()
#
#
# file = '/Users/maximgran/Desktop/rw/gg'
# statinfo = os.stat(file)
# file_size = statinfo.st_size
# text_file = file_get_contents(file)
# print(Crypt.crypt_md5(text_file))
# print(Crypt.crypt_sha1(text_file))
# print(Crypt.crypt_sha256(text_file))
# print(file_size)

"""
gg
size 381
md5 c8978e5c748e6e9c0b583d33970f7f17
sha1 77340fdc82872b83d77b74912f5b101c9a840a17
sha256 4e4dd3d8b26de75f3521269fe9b43616708e43d04ab0083f25f0a3a07e770fd9
"""