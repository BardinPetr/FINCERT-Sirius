from FilePack import FileFinder
from MailPack import MailFinder
from NetPack import NetFinder
from time import sleep
import platform


def run(data, cb):
    cb({"text": "Начато сканирование", "title": "Сканирование", "color": "success"}, 1)
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
            cb({"text": "Сканирование реестра не разрешено на %s" % ps, "title": "Система", "color": "warning"}, 1)
    if 'ram' in data:
        pass
    sleep(0.5)
    cb({"text": "Сканирование окончено", "title": "Сканирование", "color": "success"}, 1)
    sleep(0.5)
    cb(res, 2)
