# PyInstaller one-dir — Bereket Defter masaüstü (CI: windows-latest). Çıktı: dist/BereketDefter/ (BereketDefter.exe + _internal/)
# win-app kanalı bu klasörün fcpack zip'idir (python -m fccore.fcpack), win-setup kanalı NSIS kurulumu (paket/kurulum.nsi).
import os
from PyInstaller.utils.hooks import collect_data_files

KOK = os.path.abspath(os.path.join(SPECPATH, '..'))
SRC = os.path.join(KOK, 'masaustu')
datas = [(os.path.join(SRC, 'assets'), 'assets')]
datas += collect_data_files('fccore')            # yazı tipleri + lisanslar (ZORUNLU)

a = Analysis([os.path.join(SRC, 'main.py')], pathex=[SRC], binaries=[], datas=datas,
             hiddenimports=['PySide6.QtSvg', 'PySide6.QtPrintSupport', 'fc_agent', 'lan', 'notlar', 'surum'],
             excludes=['tkinter', 'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets', 'PySide6.QtQml', 'PySide6.QtQuick',
                       'PySide6.Qt3DCore', 'PySide6.QtMultimedia', 'PySide6.QtCharts', 'PySide6.QtDataVisualization'],
             noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='BereketDefter', console=False, debug=False, strip=False, upx=False,
          icon=os.path.join(SRC, 'assets', 'logo.ico'), version=None)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='BereketDefter')
