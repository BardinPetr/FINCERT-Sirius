from datetime import datetime, timedelta, timezone
from utils.encryption import get_cred
from FilePack import ReadFile, Crypt
from pathlib import Path
import platform
import re
import os


def days_from_modifed(s):  # Подсчет дней с последней модификации файла
    path = Path(s)
    statResult = path.stat()
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    modified = epoch + timedelta(seconds=statResult.st_mtime)
    return (datetime.today().utcnow().date() - modified.date()).days


def find(data, cb):
    """
        Поиск полного пути до файла.
        :param name: Имя целевого файла
        :param path: Коренной путь поиска
        :return: путь
    """
    dfm = int(get_cred()['filetime'] or 10)

    root_start = get_cred()['rootpath'] \
        if get_cred()['data'] else '/'  # Стартовый корень от которого мы начинаем поиск.
    flag = False
    if platform.system() == 'Windows':
        root_start = 'C:\\' if root_start == '/' else root_start
        flag = True

    result = dict()  # Результат нашей проверки.

    for root, dirs, files in os.walk(root_start):
        for file in files:
            file_inf = file  # Изначальное имя файла
            file = os.path.join(root, file)

            if flag and not os.access(file, os.R_OK):  # Файлы, которые нельзя, прочесть будут пропущены !!!
                continue

            if not os.path.isfile(file) or os.path.isdir(file):  # Является ли file  файлом или директорией.
                continue

            if days_from_modifed(
                    file) > dfm:  # Сколько времени прошло с последнего изменения файла. Если более указанного числа дней, то пропустим
                continue

            check_name = False

            for t in data:
                check_name = (t['name'] == file_inf or
                              (t['name'].startswith('regexp/') and re.match(t['name'][7:-1], file_inf))) or check_name

            if check_name:
                statinfo = os.stat(file)
                file_size = statinfo.st_size  # Размер файла
                path = os.path.join(root, file)

                try:
                    file_text = ReadFile.file_get_contents(file)  # Содержимое файла
                except MemoryError:
                    continue
                except PermissionError:
                    continue

                for t in data:  # Обход данных из бюллетени
                    if int(t['size']) == file_size:
                        if (t['md5'] and t['md5'] == Crypt.crypt_md5(file_text)) or \
                                (t['sha1'] and t['sha1'] == Crypt.crypt_sha1(file_text)) or \
                                (t['sha256'] and t['sha256'] == Crypt.crypt_sha256(file_text)):
                            result[file_inf] = path
                            cb.log('Найден файл: ' + result[file_inf])
    return result
