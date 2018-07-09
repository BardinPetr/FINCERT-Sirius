from FilePack import FileFinder
from MailPack import MailFinder
from NetPack import NetFinder


def run(data, cb):
    res = {}
    if 'file' in data:
        res['file'] = FileFinder.find(data['file'], cb)
    if 'mail' in data:
        res['mail'] = MailFinder.find(data['mail'], cb)
    if 'net' in data:
        res['net'] = NetFinder.find(data['net'], cb)
    if 'reg' in data:
        pass
    if 'ram' in data:
        pass
    cb(res)
