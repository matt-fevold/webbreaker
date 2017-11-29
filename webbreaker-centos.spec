# -*- mode: python -*-

block_cipher = None

a = Analysis(['webbreaker/__main__.py'],
             pathex=['/opt/webbreaker/webbreaker/__main__.py','/usr/lib/python2.7/site-packages'],
             binaries=[],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='webbreaker-cli',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
