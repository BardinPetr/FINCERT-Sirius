from cryptography.fernet import Fernet
from itertools import cycle
from pathlib import Path
from os import path
import base64
import json

home = str(Path.home())


def set_cred(cred):
    key = Fernet.generate_key()
    xk = base64.urlsafe_b64encode((10 * home)[:32].encode('utf-8'))
    open(path.join(home, '.xkstorage'), 'w').write(str(Fernet(xk).encrypt(key)))
    open(path.join(home, '.xstorage'), 'w').write(str(Fernet(key).encrypt(json.dumps(cred).encode('utf-8'))))


def get_cred():
    key = Fernet(home).decrypt(open(path.join(home, '.xkstorage'), 'r').readline())
    return json.loads(Fernet(key).decrypt(open(path.join(home, '.xstorage'), 'r').readline()))


set_cred(("121", "234"))
print(get_cred())
