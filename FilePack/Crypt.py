from hashlib import sha1, sha256, md5


def crypt_md5(s):
    return md5(s).hexdigest()


def crypt_sha256(s):
    return sha256(s).hexdigest()


def crypt_sha1(s):
    return sha1(s).hexdigest()
