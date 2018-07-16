import os
import time

root_start = '/'


def run():
    cnt = 0
    start_time = time.time()
    for root, dirs, files in os.walk(root_start):
        for file in files:
            if not os.path.isfile(file) or os.path.isdir(file):  # Является ли file  файлом или директорией.
                continue
                # statinfo = os.stat(file)
            # file_size = statinfo.st_size  # Размер файла
    print(time.time() - start_time)


run()