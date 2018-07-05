from FilePack import Crypt, ReadFile
import os
print(Crypt.crypt_md5(ReadFile.file_get_contents('/Users/maximgran/Desktop/ticket_346950671.pdf')))
statinfo = os.stat('/Users/maximgran/Desktop/ticket_346950671.pdf')
file_size = statinfo.st_size
print(file_size)