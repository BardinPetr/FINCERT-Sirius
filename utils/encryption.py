from cryptography.fernet import Fernet
from pathlib import Path
from os import path
import datetime
import base64
import json

home = str(Path.home())


def PyInit_storage():
    pass


def set_cred(cred):
    key = Fernet.generate_key()
    open(path.join(home, '.xkstorage'), 'w').write(
        Fernet(base64.urlsafe_b64encode((10 * home)[:32].encode('utf-8'))).encrypt(key).decode('utf-8'))
    open(path.join(home, '.xstorage'), 'w').write(Fernet(key).encrypt(json.dumps(cred).encode('utf-8')).decode('utf-8'))


def get_cred():
    key = Fernet(base64.urlsafe_b64encode((10 * home)[:32].encode('utf-8'))).decrypt(
        open(path.join(home, '.xkstorage'), 'r').read().encode('utf-8'))
    return json.loads(Fernet(key).decrypt(open(path.join(home, '.xstorage'), 'r').read().encode('utf-8')))


class EncryptedWay:
    def __init__(self):
        pass

    @staticmethod
    def gen_k(k=0):
        a = datetime.datetime.now() - datetime.timedelta(minutes=k)
        key = "{}/{}/{}@#{}:{}".format(a.day, a.month, a.year, a.hour, a.minute) * 4
        return key[:32]

    def decrypt(self, x, k=0):
        key = EncryptedWay.gen_k(k)
        f = Fernet(base64.b64encode(key.encode()))
        try:
            d = f.decrypt(x).decode()
            if d.startswith('MSG'):
                return json.loads(d[3:])
            raise Exception
        except:
            if k < 2:
                return self.decrypt(x, k + 1)
        return None

    def encrypt(self, x):
        pass
