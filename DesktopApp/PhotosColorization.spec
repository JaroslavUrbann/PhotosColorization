# -*- mode: python -*-
from kivy.deps import sdl2, glew
import os

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Jaroslav Urban\\Desktop\\DesktopApp_'],
             binaries=[],
             datas=[],
             hiddenimports=['pywt._extensions._cwt', 'win32file', 'win32timezone'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz, Tree(os.getcwd()),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='PhotosColorization',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
