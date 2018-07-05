from FilePack import FileFinder


def run(data):
    if 'mail' in data:
        pass
    if 'net' in data:
        pass
    if 'file' in data:
        ResArr = FileFinder.find(data['file'])
        for i in ResArr:
            print(i)
    if 'register' in data:
        pass
    if 'ram' in data:
        pass
