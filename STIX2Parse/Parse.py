from stix2 import parse
import re

a = set()

def Parse(path):
    indicator = parse(path)
    res = {
        'used': set(),
        'mail': {
            'email': [],
            'text': []
        },
        'net': {
            'ip': [],
            'url': []
        },
        'reg': {
            'keys': []
        },
        'files': [],
        'ram': {
            'procs': []
        },
        'log': []
    }

    for obj in indicator.objects:
        if obj.type == 'indicator':
            label = re.findall("=(?:\'|\".*\'|\")", obj.labels[0])[0]
            pattern = obj.pattern
            print(label, pattern)
            a.add(label)

    res['used'] = list(res['used'])
    return res


if __name__ == '__main__':
    Parse(open("/home/petr/test3/event215.json"))
    Parse(open("/home/petr/test3/event219.json"))
    Parse(open("/home/petr/test3/event220.json"))
    Parse(open("/home/petr/test3/event222.json"))
    print(a)
