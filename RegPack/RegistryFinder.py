from winreg import *

registry_roots = {
    "HKEY_CLASSES_ROOT": 2147483648,
    "HKEY_CURRENT_CONFIG": 2147483653,
    "HKEY_CURRENT_USER": 2147483649,
    "HKEY_DYN_DATA": 2147483654,
    "HKEY_LOCAL_MACHINE": 2147483650,
    "HKEY_PERFORMANCE_DATA": 2147483652,
    "HKEY_USERS": 2147483651
}


def is_kv_exists(key, value):
    res = False

    path = key.split('\\')
    root, xkey = path[0], path[-1]
    path = "\\".join(path[1:-1])

    try:
        a_reg = ConnectRegistry(None, registry_roots[root])
        a_key = OpenKey(a_reg, path)
        for i in range(1024):
            n, v, t = EnumValue(a_key, i)
            if xkey == n and value == v:
                res = True
                break
        CloseKey(a_key)
        CloseKey(a_reg)
    except Exception as ex:
        pass
    return res


def find(data, cb):
    res = []
    for i in data['keys']:
        cb.log('[REGISTRY] Trying key: %s' % i['key'])
        r = is_kv_exists(i['key'], i['val'])
        cb.log('FOUND' if r else 'NOT FOUND')
        res += [i['key']] if r else []
    return res


'''
print(find({"keys": [
    {"key": r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\a", "val": 'a'},
    {"key": r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\a", "val": 'ba'},
    {"key": r"HKEY_CURRENT_USER\Softarne\Microsoft\Windows\CurrentVersion\Run\a", "val": 'a'},
    {"key": r"HKEY_CURRE_USER\Software\Microsoft\Windows\CurrentVersion\Run\a", "val": 'a'}
]}, print))
'''