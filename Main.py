from FilePack import FileFinder
from MailPack import MailFinder


def run(data, cb):
    res = {}
    if 'file' in data:
        res['file'] = FileFinder.find(data['file'])
    if 'mail' in data:
        res['mail'] = MailFinder.find(data['mail'])
    if 'net' in data:
        pass
    if 'reg' in data:
        pass
    if 'ram' in data:
        pass
    cb(res)
