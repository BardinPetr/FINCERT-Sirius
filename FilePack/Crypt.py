from passlib.hash import sha256_crypt, md5_crypt, sha1_crypt


def crypt_md5(s):
    return md5_crypt.hash(s)


def crypt_sha256(s):
    return sha256_crypt.hash(s)


def crypt_sha1(s):
    return sha1_crypt.hash(s)
