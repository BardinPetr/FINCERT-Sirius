from FilePack import FileFinder
from MailPack import MailFinder
from NetPack import NetFinder
from time import sleep
import platform


def run(data, cb):
    cb({"text": "Scan started", "title": "SCAN", "color": "success"}, 1)
    sleep(0.5)
    res = {}
    if 'files' in data:
        res['file'] = FileFinder.find(data['files'], cb)
    if 'mail' in data:
        res['mail'] = MailFinder.find(data['mail'], cb)
    if 'net' in data:
        NetFinder.clear()
        res['net'] = NetFinder.find(data['net'], cb)
    if 'reg' in data:
        ps = platform.system()
        if ps == 'Windows':
            from RegPack import RegistryFinder
            res['reg'] = RegistryFinder.find(data['reg'], cb)
        else:
            cb({"text": "Scanning registry isn't allowed on %s" % ps, "title": "SYSTEM", "color": "warning"}, 1)
    if 'ram' in data:
        pass
    sleep(0.5)
    cb({"text": "Scan finished", "title": "SCAN", "color": "success"}, 1)
    sleep(0.5)
    cb(res, 2)
