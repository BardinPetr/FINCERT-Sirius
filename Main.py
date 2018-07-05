import FilePack as fp


def run(data, cb):
    res = {}
    if 'mail' in data:
        pass
    if 'net' in data:
        pass
    if 'file' in data:
        res['file'] = fp.FileFinder.find(data['file'])
    if 'reg' in data:
        pass
    if 'ram' in data:
        pass
    cb(res)
