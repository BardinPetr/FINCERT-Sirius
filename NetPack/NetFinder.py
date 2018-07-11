"""
This code was verified on Ubuntu 17.10, Windows 10(English), Mac OSX
"""

from scapy.all import *
import datetime
import socket

table = {num: name[8:] for name, num in vars(socket).items() if name.startswith("IPPROTO")}
res = {'format': [], 'non_format': []}


def pkt_callback(pkt, data, cb):
    for pack in pkt:

        try:
            ip_source = pack[IP].src
            ip_destination = pack[IP].dst
        except IndexError:
            continue

        tm = pack[IP].time
        value = datetime.datetime.fromtimestamp(tm)
        tm = value.strftime('%Y-%m-%d %H:%M:%S') # Time when packet came
        tp = table[int(pkt[IP].proto)].lower()

        if ip_source in data['ip']:
            res['non_format'].append({'ip': ip_source, 'time': tm, 'type': tp + ' to'})
            s = 'At {} -- [{}] {} -> {} '.format(tm, tp, ip_source, ip_destination)
            res['format'].append(s)
            cb(s)

        if ip_destination in data['ip']:
            res['non_format'].append({'ip': ip_destination, 'time': tm, 'type': tp + ' from'})
            s = 'At {} -- [{}] {} -> {} '.format(tm, tp, ip_source, ip_destination)
            res['format'].append(s)
            cb(s)

        if ip_source in data['ip_url']:
            res['non_format'].append({'ip': ip_source, 'time': tm, 'type': tp + ' to'})
            s = 'At {} -- [{}] {}'.format(tm, tp, data['ip_url'][ip_source])
            res['format'].append('At {} -- [{}] {}'.format(tm, tp, data['ip_url'][ip_source]))
            cb(s)

        if ip_destination in data['ip_url']:
            res['non_format'].append({'ip': ip_source, 'time': tm, 'type': tp + ' from'})
            s = 'At {} -- [{}] {}'.format(tm, tp, data['ip_url'][ip_destination])
            res['format'].append('At {} -- [{}] {}'.format(tm, tp, data['ip_url'][ip_destination]))
            cb(s)


def find(data, cb):
    dt = ({'ip': data['ip'], 'time': data['time'], 'ip_url': {}})

    for i in data['url']:
        dt['ip_url'][socket.gethostbyname(i)] = i  # Get ip by host name

    sniff(prn=lambda x: pkt_callback(x, dt, cb), store=0,
          timeout=dt[
                      'time'] * 60)  # Dt - database, Cb - callback, store=0 means that we won't store our res, timeout in seconds
    return res