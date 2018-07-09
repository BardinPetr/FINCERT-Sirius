import datetime
from cryptography.fernet import Fernet
import base64

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


def gen_k(k=0):
    a = datetime.datetime.now()
    key = "Something always goes wrong at: {}/{}/{} @ {}:{}".format(a.day, a.month, a.year, a.hour, a.minute + k)
    return key


from cryptography.fernet import Fernet

f = Fernet(base64.b64encode('9/7/2018@#11:509/7/2018@#11:509/'.encode()))
print(f.decrypt(b"gAAAAABbQygdBLV_pRSvdDFU1XuuKtMBBFVgbOrnzZM0MP-ieKKrHBcqjEfasF6gGhugshDzx2mtbQlEaIJ5C7nn7vY8qCp-Vw=="))
