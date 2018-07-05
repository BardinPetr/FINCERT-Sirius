import ReadFile
import Crypt
import os
import platform


def find(data):
    """
        Поиск полного пути до файла.
        :param name: Имя целевого файла
        :param path: Коренной путь поиска
        :return: путь
    """
    root = '/'
    if platform.system() == 'Windows':
        root = 'C:\\'

    for root, dirs, files in os.walk(root):
        for file in files:

            statinfo = os.stat(file)
            file_size = statinfo.st_size
            path = os.path.join(root, file)

            for t in data:
                if t[0][0] == file:

                if t[0][1] == file_size:
                    if t[0][2]['MD5'] == Crypt.crypt_md5(ReadFile.file_get_contents(file)):

                    if t[0][2]['SHA1'] == Crypt.


"""
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result
"""
