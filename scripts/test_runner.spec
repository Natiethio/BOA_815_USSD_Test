# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['test_app.py'],
    pathex=[],
    binaries=[],
    datas=[('My_Account', 'My_Account'), ('Transfer', 'Transfer'), ('Transfer_otherBank', 'Transfer_otherBank'), ('Transfer_to_own', 'Transfer_to_own'), ('AirTime', 'AirTime'), ('Exchange_Rates', 'Exchange_Rates'), ('Helpers', 'Helpers'), ('USSD_Test_Script.xlsx', '.')],
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
    name='test_runner',
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
)
