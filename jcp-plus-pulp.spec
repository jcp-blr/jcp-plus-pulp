# -*- mode: python -*-
# vi: set ft=python :
import os
import platform
import shlex
import subprocess
from pathlib import Path

import jcp_plus_pulp_core
import flask_restx


def build_analysis(name, location, binaries=[], datas=[], hiddenimports=[]):
    name_py = name.replace("-", "_")
    location_candidates = [
        location / f"{name_py}/__main__.py",
        location / f"src/{name_py}/__main__.py",
    ]
    try:
        location = next(p for p in location_candidates if p.exists())
    except StopIteration:
        raise Exception(f"Could not find {name} location from {location_candidates}")

    return Analysis(
        [location],
        pathex=[],
        binaries=binaries,
        datas=datas,
        hiddenimports=hiddenimports,
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
    )


def build_collect(analysis, name, console=True):
    """Used to build the COLLECT statements for each module"""
    pyz = PYZ(analysis.pure, analysis.zipped_data)
    exe = EXE(
        pyz,
        analysis.scripts,
        exclude_binaries=True,
        name=name,
        debug=False,
        strip=False,
        upx=True,
        console=console,
        entitlements_file=entitlements_file,
        codesign_identity=codesign_identity,
    )
    return COLLECT(
        exe,
        analysis.binaries,
        analysis.zipfiles,
        analysis.datas,
        strip=False,
        upx=True,
        name=name,
    )


# Get the current release version
current_release = subprocess.run(
    shlex.split("git describe --tags --abbrev=0"),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    encoding="utf8",
).stdout.strip()
print("bundling jcp-plus-pulp version " + current_release)

# Get entitlements and codesign identity
entitlements_file = Path(".") / "scripts" / "package" / "entitlements.plist"
codesign_identity = os.environ.get("APPLE_PERSONALID", "").strip()
if not codesign_identity:
    print("Environment variable APPLE_PERSONALID not set. Releases won't be signed.")

jcp_plus_pulp_core_path = Path(os.path.dirname(jcp_plus_pulp_core.__file__))
restx_path = Path(os.path.dirname(flask_restx.__file__))

aws_location = Path("jcp-plus-pulp-server")
jcp_plus_pulp_qt_location = Path("jcp-plus-pulp-qt")
awa_location = Path("jcp-plus-pulp-monitor-away")
aww_location = Path("jcp-plus-pulp-monitor-window")
awi_location = Path("jcp-plus-pulp-monitor-input")
aw_sync_location = Path("jcp-plus-pulp-sync")

if platform.system() == "Darwin":
    icon = jcp_plus_pulp_qt_location / "media/logo/logo.icns"
else:
    icon = jcp_plus_pulp_qt_location / "media/logo/logo.ico"

jcp_plus_pulp_qt_a = build_analysis(
    "jcp-plus-pulp-qt",
    jcp_plus_pulp_qt_location,
    binaries=[],
    datas=[
        (jcp_plus_pulp_qt_location / "resources/jcp-plus-pulp-qt.desktop", "jcp_plus_pulp_qt/resources"),
        (jcp_plus_pulp_qt_location / "media", "jcp_plus_pulp_qt/media"),
    ],
)
jcp_plus_pulp_server_a = build_analysis(
    "jcp-plus-pulp-server",
    aws_location,
    datas=[
        (restx_path / "templates", "flask_restx/templates"),
        (restx_path / "static", "flask_restx/static"),
        (jcp_plus_pulp_core_path / "schemas", "jcp_plus_pulp_core/schemas"),
    ],
)
jcp_plus_pulp_monitor_away_a = build_analysis(
    "jcp_plus_pulp_monitor_away",
    awa_location,
    hiddenimports=[
        "Xlib.keysymdef.miscellany",
        "Xlib.keysymdef.latin1",
        "Xlib.keysymdef.latin2",
        "Xlib.keysymdef.latin3",
        "Xlib.keysymdef.latin4",
        "Xlib.keysymdef.greek",
        "Xlib.support.unix_connect",
        "Xlib.ext.shape",
        "Xlib.ext.xinerama",
        "Xlib.ext.composite",
        "Xlib.ext.randr",
        "Xlib.ext.xfixes",
        "Xlib.ext.security",
        "Xlib.ext.xinput",
        "pynput.keyboard._xorg",
        "pynput.mouse._xorg",
        "pynput.keyboard._win32",
        "pynput.mouse._win32",
        "pynput.keyboard._darwin",
        "pynput.mouse._darwin",
    ],
)
jcp_plus_pulp_monitor_input_a = build_analysis("jcp_plus_pulp_monitor_input", awi_location)
jcp_plus_pulp_monitor_window_a = build_analysis(
    "jcp_plus_pulp_monitor_window",
    aww_location,
    binaries=[
        (
            aww_location / "jcp_plus_pulp_monitor_window/jcp-plus-pulp-monitor-window-macos",
            "jcp_plus_pulp_monitor_window",
        )
    ]
    if platform.system() == "Darwin"
    else [],
    datas=[
        (aww_location / "jcp_plus_pulp_monitor_window/printAppStatus.jxa", "jcp_plus_pulp_monitor_window")
    ],
)
jcp_plus_pulp_sync_a = build_analysis(
    "jcp_plus_pulp_sync", aw_sync_location, hiddenimports=["desktop_notifier.resources"]
)

# https://pythonhosted.org/PyInstaller/spec-files.html#multipackage-bundles
# MERGE takes a bit weird arguments, it wants tuples which consists of
# the analysis paired with the script name and the bin name
MERGE(
    (jcp_plus_pulp_server_a, "jcp-plus-pulp-server", "jcp-plus-pulp-server"),
    (jcp_plus_pulp_qt_a, "jcp-plus-pulp-qt", "jcp-plus-pulp-qt"),
    (jcp_plus_pulp_monitor_away_a, "jcp-plus-pulp-monitor-away", "jcp-plus-pulp-monitor-away"),
    (jcp_plus_pulp_monitor_window_a, "jcp-plus-pulp-monitor-window", "jcp-plus-pulp-monitor-window"),
    (jcp_plus_pulp_monitor_input_a, "jcp-plus-pulp-monitor-input", "jcp-plus-pulp-monitor-input"),
    (jcp_plus_pulp_sync_a, "jcp-plus-pulp-sync", "jcp-plus-pulp-sync"),
)


# jcp-plus-pulp-server
aws_coll = build_collect(jcp_plus_pulp_server_a, "jcp-plus-pulp-server")

# jcp-plus-pulp-monitor-window
aww_coll = build_collect(jcp_plus_pulp_monitor_window_a, "jcp-plus-pulp-monitor-window")

# jcp-plus-pulp-monitor-away
awa_coll = build_collect(jcp_plus_pulp_monitor_away_a, "jcp-plus-pulp-monitor-away")

# jcp-plus-pulp-qt
awq_coll = build_collect(
    jcp_plus_pulp_qt_a,
    "jcp-plus-pulp-qt",
    console=False if platform.system() == "Windows" else True,
)

# jcp-plus-pulp-monitor-input
awi_coll = build_collect(jcp_plus_pulp_monitor_input_a, "jcp-plus-pulp-monitor-input")

aw_sync_coll = build_collect(jcp_plus_pulp_sync_a, "jcp-plus-pulp-sync")

if platform.system() == "Darwin":
    app = BUNDLE(
        awq_coll,
        aws_coll,
        aww_coll,
        awa_coll,
        awi_coll,
        aw_sync_coll,
        name="JCP+ PULP.app",
        icon=icon,
        bundle_identifier="net.jcp-plus-pulp.JCPPLUSPULP",
        version=current_release.lstrip("v"),
        info_plist={
            "NSPrincipalClass": "NSApplication",
            "CFBundleExecutable": "MacOS/jcp-plus-pulp-qt",
            "CFBundleIconFile": "logo.icns",
            "NSAppleEventsUsageDescription": "Please grant access to use Apple Events",
            # This could be set to a more specific version string (including the commit id, for example)
            "CFBundleVersion": current_release.lstrip("v"),
            # Replaced by the 'version' kwarg above
            # "CFBundleShortVersionString": current_release.lstrip('v'),
        },
    )
