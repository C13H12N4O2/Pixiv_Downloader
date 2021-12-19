# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Pixiv_Downloader/PixivDownloader.py'],
             pathex=[],
             binaries=[],
             datas=[('Pixiv_Downloader/Resources/*', 'Resources/')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='PixivDownloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
app = BUNDLE(exe,
             name='PixivDownloader.app',
             icon='Pixiv_Downloader/Resources/DefaultUserIcon.icns',
             bundle_identifier=None,
             version='1.0.0')
