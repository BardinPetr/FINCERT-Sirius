from FilePack import ReadFile, Crypt
import os
import time


def run():
    file = '/Users/maximgran/Desktop/rw/gg'
    statinfo = os.stat(file)
    file_size = statinfo.st_size  # Размер файла
    file_text = ReadFile.file_get_contents(file)
    print(file)
    print(file_size)
    print(Crypt.crypt_md5(file_text))
    print(Crypt.crypt_sha1(file_text))
    print(Crypt.crypt_sha256(file_text))
    print(time.time())

run()
