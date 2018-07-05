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
    root_start = '/'
    if platform.system() == 'Windows':
        root_start = 'C:\\'
    result = dict()

    for root, dirs, files in os.walk(root_start):
        for file in files:

            statinfo = os.stat(file)
            file_size = statinfo.st_size
            path = os.path.join(root, file)
            file_text = ReadFile.file_get_contents(file)

            for t in data:
                if t[0][1] == file_size:
                    if t[0][2]['MD5'] == Crypt.crypt_md5(file_text):
                        if t[0][2]['SHA1'] == Crypt.crypt_sha1(file_text):
                            if t[0][2]['SHA256'] == Crypt.crypt_sha256(file_text):
                                result[file] = path

    return result


"""
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result
"""
