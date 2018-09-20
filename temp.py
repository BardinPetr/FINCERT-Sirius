from FilePack import ReadFile, Crypt
import os
import time


def run(file):
    statinfo = os.stat(file)
    file_size = statinfo.st_size  # Размер файла
    file_text = ReadFile.file_get_contents(file)
    print(file)
    print(file_size)
    print(Crypt.crypt_md5(file_text))
    print(Crypt.crypt_sha1(file_text))
    print(Crypt.crypt_sha256(file_text))
    print()

run('/mnt/Data/гыыыы/65757656757687.jpg')
run('/mnt/Data/гыыыы/F-YHN__HoP_UJFUH.jpg')
run('/mnt/Data/гыыыы/random5293ui8jrwh89wguofh.jpg')
run('/mnt/Data/гыыыы/чотоплохосовсем.jpg')
