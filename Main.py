from FilePack import FileFinder
from MailPack import MailFinder
from NetPack import NetFinder
from time import sleep
import platform
from RamPack import RamFinder


# TODO remove Flag

def run(data, cb):
    is_valid_data = False
    for i in data:
        if i == 'files':
            for j in data[i]:
                for k in j:
                    if k != 'size':
                        is_valid_data = len(j[k]) or is_valid_data
        else:
            for j in data[i]:
                is_valid_data = len(data[i][j]) or is_valid_data

    if is_valid_data:
        res = {}
        cb("", 4)
        sleep(0.5)
        cb({"text": "Начато сканирование", "title": "Сканирование", "color": "success"}, 1)

        is_valid_data = False
        if 'files' in data:
            res['file'] = FileFinder.find(data['files'], cb)

        if 'mail' in data:
            for i in data['mail']:
                is_valid_data = len(data['mail'][i]) or is_valid_data

        if is_valid_data and 'mail' in data:
            res['mail'] = MailFinder.find(data['mail'], cb)

        # Проверка на заполнение поля Сети.

        if 'net' in data:
            is_valid_data = False
            for i in data['net']:
                is_valid_data = len(data['net'][i]) or is_valid_data

        if is_valid_data and 'net' in data:
            NetFinder.clear()
            res['net'] = NetFinder.find(data['net'], cb)

        # Проверка на заполнение поля Реестра.

        if 'reg' in data:
            is_valid_data = bool(len(data['reg']['keys']))

        if is_valid_data and 'reg' in data:
            ps = platform.system()
            if ps == 'Windows':
                from RegPack import RegistryFinder
                res['reg'] = RegistryFinder.find(data['reg'], cb)
            else:
                cb({"text": "Сканирование реестра не разрешено на %s" % ps, "title": "Система", "color": "warning"}, 1)

        # TODO Проверка на заполнение поля ОЗУ.

        is_valid_data = False
        if 'ram' in data:
            for i in data['ram']:
                is_valid_data = len(data['ram'][i]) or is_valid_data

        if is_valid_data and 'ram' in data:
            res['ram'] = RamFinder.find(data['ram'], cb)

        sleep(0.5)
        cb({"text": "Сканирование окончено", "title": "Сканирование", "color": "success"}, 1)
        sleep(0.5)
        cb(res, 2)
    else:
        cb({"text": "Данные не введены", "title": "Ошибка ввода данных", "color": "error"}, 1)
