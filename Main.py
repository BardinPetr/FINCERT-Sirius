from FilePack import FileFinder
from MailPack import MailFinder
from NetPack import NetFinder
import platform


def run(data, cb):
    res = {}
    if 'files' in data:
        res['file'] = FileFinder.find(data['files'], cb)
    if 'mail' in data:
        res['mail'] = MailFinder.find(data['mail'], cb)
    if 'net' in data:
        res['net'] = NetFinder.find(data['net'], cb)
    if 'reg' in data and platform.system() == 'Windows':
        res['reg'] = NetFinder.find(data['reg'], cb)
    if 'ram' in data:
        pass
    cb(res)
