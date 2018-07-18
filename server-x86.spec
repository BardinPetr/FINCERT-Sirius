# -*- mode: python -*-

block_cipher = None
import os

a = Analysis(['server.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[(os.getcwd()+'\\temp', '.\\temp'), 
             (os.getcwd()+'\\templates', '.\\templates'), 
             (os.getcwd()+'\\static', '.\\static'),
             (os.getcwd()+'\\icon.ico', '.')],
             hiddenimports=['werkzeug'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='server',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon=os.getcwd()+'\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='app-x86')
