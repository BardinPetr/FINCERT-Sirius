import platform
import yara
import os


def find(rules, cb):
    cb("[YARA-RULES] Сканирование по YARA-правилам начато")
    result = []
    for rule in rules:
        result += run_yara(rule, cb)
    cb("[YARA-RULES] Сканирование по YARA-правилам завершено. Результат: %d" % len(result))
    return result


def run_yara(data, cb):
    """
    import "hash" rule foo {condition: filesize < 100KB and hash.md5(0, filesize) == "1f08ec19b2b667a96364f02d10e210c0"}
    :param data:
    :param cb:
    :return:
    """
    try:
        rule = yara.compile(
            source=data)  # Создание yara.Rules object
    except yara.SyntaxError:
        cb({"text": "Найдено невалидное YARA-правило!", "title": "Ошибка ввода данных", "color": "error"}, 1)
        return []
    root_start = '/home/petr/Pictures'  # Стартовый корень от которого мы начинаем поиск.
    result = list()
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
                result.append(
                    [str(rule.match(file)), file])  # Results be like [(%matched rule name%, %matched file path%)]
            # print(len(rule.match(file)))
            # print(file)
    return result
