import platform

block_cipher = None

a = Analysis(
    ["jcp_plus_pulp_monitor_window/__main__.py"],
    pathex=[],
    binaries=[("jcp_plus_pulp_monitor_window/jcp-plus-pulp-monitor-window-macos", "jcp_plus_pulp_monitor_window")] if platform.system() == "Darwin" else [],
    datas=[
        ("jcp_plus_pulp_monitor_window/printAppStatus.jxa", "jcp_plus_pulp_monitor_window"),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name="jcp-plus-pulp-monitor-window",
    debug=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="jcp-plus-pulp-monitor-window",
)
