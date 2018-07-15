from stix2 import parse


def parse(path):
    indicator = parse(path)
    print(indicator)
    res = {}
    return res


if __name__ == '__main__':
    parse(open("/home/petr/test3/event219.json"))
