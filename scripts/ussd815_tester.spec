# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['boa_ussd_test_guiupd.py'],
    pathex=[],
    binaries=[],
    datas=[('test_runner.exe', '.'), ('logo.png', '.'), ('spinner2.gif', '.'), ('USSD_Test_Script.xlsx', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ussd815_tester',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo_icon.ico'],
)
