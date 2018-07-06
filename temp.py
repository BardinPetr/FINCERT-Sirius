from FilePack import Crypt, ReadFile
import os
print(Crypt.crypt_md5(ReadFile.file_get_contents('C:\\Users\\Student\\Desktop\\rw\\version.txt')))
statinfo = os.stat('C:\\Users\\Student\\Desktop\\rw\\version.txt')
file_size = statinfo.st_size
print(file_size)