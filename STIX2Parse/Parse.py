from stix2 import parse
import re


def parse_stix(path):
    indicator = parse(path)
    qtable = {"files": ["sha1", "sha256", "md5", "filename"]}
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
            label = re.findall("=(?:['\"].+['\"])", obj.labels[0])[0][2:-1]
            patterns = {
                x.split(' = ')[0].replace('\'', '').replace('\"', ''): x.split(' = ')[1].replace('\'', '').replace('\"',
                                                                                                                   '')
                for x in re.split('\s(?:AND|OR|and|or)\s', obj.pattern[1:-1])}
            if label in qtable['files']:
                res['files'].append({
                    "name": patterns.get('file:name', "<N/A>"),
                    "sha1": patterns.get("file:hashes.sha1", "<N/A>"),
                    "sha256": patterns.get("file:hashes.sha256", "<N/A>"),
                    "md5": patterns.get("file:hashes.md5", "<N/A>")
                })
            elif label == 'ip-dst':
                res['net']['ip'] += [patterns.get('network-traffic:dst_ref.value')] \
                    if 'network-traffic:dst_ref.value' in patterns else []
            elif label == 'hostname':
                res['net']['url'] += [patterns.get('domain-name:value')] \
                    if 'domain-name:value' in patterns else []
            elif label == 'email-src':
                res['mail']['email'] += [patterns.get('email-message:from_ref')] \
                    if 'email-message:from_ref' in patterns else []
            print(label, patterns)

    res['used'] = list(res['used'])
    return res


'''
if __name__ == '__main__':
    from pprint import pprint as p
    p(Parse(open("/home/petr/test3/event222.json")))
    Parse(open("/home/petr/test3/event219.json"))
    Parse(open("/home/petr/test3/event220.json"))
    Parse(open("/home/petr/test3/event222.json"))
'''
