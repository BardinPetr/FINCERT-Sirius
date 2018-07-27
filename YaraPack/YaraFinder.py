import platform
import yara
import os


def find(data, cb):
    """
    import "hash" rule foo {condition: filesize < 100KB and hash.md5(0, filesize) == '
               '"4a00c4a612c23314b2f34c66139f4318"}
    :param data:
    :param cb:
    :return:
    """
    rule = yara.compile(
        source=data)  # Создание yara.Rules object
    root_start = '/'  # Стартовый корень от которого мы начинаем поиск.
    result = dict()
    # print(rule)
    flag = False
    if platform.system() == 'Windows':
        root_start = 'C:\\'
        flag = True

    for root, dirs, files in os.walk(root_start):
        for file in files:
            file_inf = file
            file = os.path.join(root, file)
            if len(rule.match(file)):
                result[str(rule.match(file))] = file
            # print(len(rule.match(file)))
            # print(file)
    return result
