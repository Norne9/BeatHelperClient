# -*- mode: python ; coding: utf-8 -*-
import os
import importlib

block_cipher = None
package_imports = [['cloudscraper', ['user_agent/browsers.json']]]


data_list = []
for package, files in package_imports:
    proot = os.path.dirname(importlib.import_module(package).__file__)
    data_list.extend((os.path.join(proot, f), os.path.join(package, os.path.dirname(f))) for f in files)
print(data_list)

a = Analysis(['main.py'],
             pathex=['./'],
             binaries=[],
             datas=data_list,
             hiddenimports=['wx._adv', 'wx._html', 'wx._xml', 'cloudscraper.interpreters.native'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='BeatHelper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='icon.ico',
          console=False)