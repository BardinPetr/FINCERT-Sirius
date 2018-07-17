from cx_Freeze import setup, Executable
import os

_, dirs, files = next(os.walk(os.getcwd()))
include_files = files + list(map(lambda x: x + '', dirs))
#pkgs = ['webbrowser', 'hashlib', 'os', 'platform', 'datetime', 'time', 'pathlib', 'imaplib', 'email', 're', 'locale', 'socket', 'logging', 'json', 'sys', 'pprint', 'math', 'collections', 'base64', 'functools', 'threading', 'struct', 'errno']
pkgs = list(map(lambda x: x.strip(), open("requirements.txt").readlines()))

setup(
    name = 'FINCERT-SCANNER',
    version = '0.1.0',
    data_files = include_files,
    options = {"build_exe": {
        #'include_files': include_files,
        'include_msvcr': True,
        #'packages': pkgs
    }},
    executables = [Executable('server.py')]
)
