"""
This code was verified on Ubuntu 17.10, Windows 10(English), Mac OSX
"""

from utils.encryption import get_cred
from itertools import groupby
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
        tm = value.strftime('%Y-%m-%d %H:%M:%S')  # Time when packet came
        tp = table[int(pkt[IP].proto)].lower()

        if ip_source in data['ip']:
            res['non_format'].append({'ip': ip_source, 'time': tm, 'type': tp + ' to'})
            s = 'Дата: {} -- [{}] {} -> {} '.format(tm, tp, ip_source, ip_destination)
            res['format'].append(s)
            cb(s)

        if ip_destination in data['ip']:
            res['non_format'].append({'ip': ip_destination, 'time': tm, 'type': tp + ' from'})
            s = 'Дата: {} -- [{}] {} -> {} '.format(tm, tp, ip_source, ip_destination)
            res['format'].append(s)
            cb(s)

        if ip_source in data['ip_url']:
            res['non_format'].append({'ip': ip_source, 'time': tm, 'type': tp + ' to'})
            s = 'Дата: {} -- [{}] {}'.format(tm, tp, data['ip_url'][ip_source])
            res['format'].append(s)
            cb(s)

        if ip_destination in data['ip_url']:
            res['non_format'].append({'ip': ip_source, 'time': tm, 'type': tp + ' from'})
            s = 'Дата: {} -- [{}] {}'.format(tm, tp, data['ip_url'][ip_destination])
            res['format'].append(s)
            cb(s)


def clear():
    res['format'] = []
    res['non_format'] = []


def postprocess_data():
    f = lambda x: x.split(' -- ')[1]
    return list(map(lambda x: (x[0], list(x[1])), groupby(sorted(res['format'], key=f), key=f)))


def find(data, cb):
    udata = get_cred()
    if not udata['data']:
        cb({"text": "Время не настроено в разделе НАСТРОЙКИ", "title": "Ошибка анализа сети", "color": "error"}, 1)
    else:
        dt = ({'ip': data['ip'], 'time': udata['snifftime'], 'ip_url': {}})
        for i in data['url']:
            try:
                dt['ip_url'][socket.gethostbyname(i)] = i  # Get ip by host name
            except socket.gaierror:
                continue

        try:
            sniff(prn=lambda x: pkt_callback(x, dt, cb), store=0,
                  timeout=int(
                      dt['time']) * 60)  # Dt - database, Cb - callback, store=0 means that we won't store our res
        except PermissionError:
            cb({"text": "Анализ сети не разрешен", "title": "Системная ошибка", "color": "error"}, 1)
        except Exception as ex:
            cb({"text": ex, "title": "Ошибка анализа сети", "color": "error"}, 1)
    return postprocess_data()
