import subprocess


def find(data, cb):
    res = []
    processes = data["procs"]
    real_processes = []

    for real_proc in [line.split() for line in subprocess.check_output("tasklist").splitlines()]:
        if (len(real_proc) > 0):
            real_processes.append(str(real_proc[0].decode('cp866')))  # вывод списков

    result = list(set((real_processes)) & set(processes))
    for r in result:
        cb("Наличие процесса в системе: {}".format(str(r)))
    str_result = ", ".join(result, )
    res.append("Наличие процесса в системе: {}".format(str_result))

    return res
