import ReadFile
import Crypt
import os


def find(name, path):
    """
    Поиск полного пути до файла.
    :param name: Имя целевого файла
    :param path: Коренной путь поиска
    :return: путь
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def find_all(name, path):
    """
    Если требуется найти все совпадения в системе.
    :param name: Имя целевого файла
    :param path: Коренной путь поиска
    :return: путь
    """
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


nameG = input()
pathG = input()
md5 = Crypt.crypt_md5(ReadFile.file_get_contents(find(nameG, pathG)))
print(md5)
