import os
import ReadFile
import Crypt


# На Windows не проверял.

# Поиск полного пути до файла. На вход: Имя, коренной путь поиска.

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


# Если требуется найти все совпадения в системе.
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


nameG = input()
pathG = input()
md5 = Crypt.crypt_md5(ReadFile.file_get_contents(find(nameG, pathG)))
print(md5)
