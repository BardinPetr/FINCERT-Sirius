from FilePack import FileFinder
from MailPack import MailFinder
from NetPack import NetFinder


def run(data, cb):
    print("PIZDA V MAIN")
    print(data)
    res = {}
    if 'files' in data:
        print("DAROVA")
        res['file'] = FileFinder.find(data['files'], cb)
    if 'mail' in data:
        res['mail'] = MailFinder.find(data['mail'], cb)
    if 'net' in data:
        res['net'] = NetFinder.find(data['net'], cb)
    if 'reg' in data:
        pass
    if 'ram' in data:
        pass
    cb(res)
