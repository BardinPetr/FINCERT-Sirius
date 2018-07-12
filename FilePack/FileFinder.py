from FilePack import ReadFile, Crypt
import os
import platform
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time


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

    print('In file finder')
    start_time = time.time()
    buf_time = time.time()

    root_start = '/'  # Стартовый корень от которого мы начинаем поиск.
    flag = False
    if platform.system() == 'Windows':
        root_start = 'C:\\'
        flag = True

    result = dict()  # Результат нашей проверки.

    file_count = 0
    overall_file_size = 0
    file_count_sys = 0
    overall_file_size_sys = 0
    count_indicators = 0

    for root, dirs, files in os.walk(root_start):
        for file in files:

            if count_indicators == len(data):  # Если все индикаторы были найдены.
                return result

            if time.time() - buf_time >= 10:
                print('Time from start: ', time.time() - start_time)
                print('Overall amount of files: ', file_count_sys)
                print('Overall files size: ', overall_file_size_sys)

                print('\n OPENED FILES: ', file_count)
                print('Residual count: ', file_count_sys - file_count)
                print('Residual size: ', overall_file_size_sys - overall_file_size)
                buf_time = time.time()

            file_inf = file  # Изначальное имя файла
            file = os.path.join(root, file)

            if not os.access(file, os.R_OK) and flag:  # Файлы, которые нельзя, прочесть будут пропущены !!!
                continue
            if not os.path.isfile(file) or os.path.isdir(file):  # Является ли file  файлом или директорией.
                continue

            statinfo = os.stat(file)
            file_size = statinfo.st_size  # Размер файла в байтах

            file_count_sys += 1
            overall_file_size_sys += file_size

            if days_from_modifed(
                    file) > 10:  # Сколько времени прошло с последнего изменения файла. Если более 10 дней, то пропустим
                continue

            if os.path.isfile(file):
                file_count += 1
                overall_file_size += file_size

            path = os.path.join(root, file)

            try:
                file_text = ReadFile.file_get_contents(file)  # Содержимое файла
            except MemoryError:
                continue
            except PermissionError:
                continue

            for t in data:  # Обход данных из бюллетени
                if int(t['size']) == file_size:
                    if t['md5'] == Crypt.crypt_md5(file_text):
                        if t['sha1'] == Crypt.crypt_sha1(file_text):
                            if t['sha256'] == Crypt.crypt_sha256(file_text):
                                count_indicators += 1
                                result[file_inf] = path
                                cb(result[file_inf] + '\n')

    return result


"""
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result
"""
