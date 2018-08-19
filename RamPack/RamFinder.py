import subprocess


def find(data, cb):
    processes = data["procs"]
    real_processes = []

    for real_proc in [line.split() for line in subprocess.check_output("tasklist").splitlines()]:
        if len(real_proc) > 0:
            real_processes.append(str(real_proc[0].decode('cp866')))  # вывод списков

    result = list(set(real_processes) & set(processes))
    for r in result:
        cb.log("Наличие процесса в системе: {}".format(str(r)))
    return result
