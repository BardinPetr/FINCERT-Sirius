import FilePack as fp


def run(data):
    if 'mail' in data:
        pass
    if 'net' in data:
        pass
    if 'file' in data:
        fp.FileFinder.find(data['file'])
    if 'register' in data:
        pass
    if 'ram' in data:
        pass
    

