from FilePack import FileFinder
from MailPack import MailFinder
from NetPack import NetFinder
from time import sleep
import platform


def run(data, cb):
    print(data)
    flag = False
    for i in data:
        if i == 'files':
            for j in data[i]:
                for k in j:
                    if k != 'size':
                        flag = len(j[k]) or flag
        else:
            for j in data[i]:
                flag = len(data[i][j]) or flag

    if flag:
        cb({"text": "Начато сканирование", "title": "Сканирование", "color": "success"}, 1)
        sleep(0.5)
        res = {}

        flag = False
        if 'files' in data:
            res['file'] = FileFinder.find(data['files'], cb)

        if 'mail' in data:
            for i in data['mail']:
                flag = len(data['mail'][i]) or flag

        if flag and 'mail' in data:
            res['mail'] = MailFinder.find(data['mail'], cb)

        # Проверка на заполнение поля Сети.

        if 'net' in data:
            flag = False
            for i in data['net']:
                flag = len(data['net'][i]) or flag

        if flag and 'net' in data:
            NetFinder.clear()
            res['net'] = NetFinder.find(data['net'], cb)

        # Проверка на заполнение поля Реестра.
        if 'reg' in data:
            flag = False
            for i in data['reg']:
                flag = len(data['net'][i]) or flag

        if flag and 'reg' in data:
            ps = platform.system()
            if ps == 'Windows':
                from RegPack import RegistryFinder
                res['reg'] = RegistryFinder.find(data['reg'], cb)
            else:
                cb({"text": "Сканирование реестра не разрешено на %s" % ps, "title": "Система", "color": "warning"}, 1)

        # Проверка на заполнение поля ОЗУ.
        flag = False
        for i in data['ram']:
            flag = len(data['ram'][i]) or flag

        if flag and 'ram' in data:
            pass

        sleep(0.5)
        cb({"text": "Сканирование окончено", "title": "Сканирование", "color": "success"}, 1)
        sleep(0.5)
        cb(res, 2)
    else:
        cb({"text": "Данные не введены", "title": "Ошибка ввода данных", "color": "error"}, 1)
