# -*- mode: python -*-
# vi: set ft=python :
import os
import platform
import shlex
import subprocess
from pathlib import Path

import aw_core
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
print("bundling activitywatch version " + current_release)

# Get entitlements and codesign identity
entitlements_file = Path(".") / "scripts" / "package" / "entitlements.plist"
codesign_identity = os.environ.get("APPLE_PERSONALID", "").strip()
if not codesign_identity:
    print("Environment variable APPLE_PERSONALID not set. Releases won't be signed.")

aw_core_path = Path(os.path.dirname(aw_core.__file__))
restx_path = Path(os.path.dirname(flask_restx.__file__))

aws_location = Path("aw-server")
aw_server_rust_location = Path("aw-server-rust")
aw_server_rust_bin = aw_server_rust_location / "target/package/aw-server-rust"
aw_sync_bin = aw_server_rust_location / "target/package/aw-sync"
aw_qt_location = Path("aw-qt")
awa_location = Path("jcp-plus-pulp-capture-afk")
aww_location = Path("jcp-plus-pulp-capture-window")
awi_location = Path("jcp-plus-pulp-capture-input")
jcp_plus_pulp_notify_location = Path("jcp-plus-pulp-notify")

if platform.system() == "Darwin":
    icon = aw_qt_location / "media/logo/logo.icns"
else:
    icon = aw_qt_location / "media/logo/logo.ico"

skip_rust = False
if not aw_server_rust_bin.exists():
    skip_rust = True
    print("Skipping Rust build because aw-server-rust binary not found.")


aw_qt_a = build_analysis(
    "aw-qt",
    aw_qt_location,
    binaries=[(aw_server_rust_bin, "."), (aw_sync_bin, ".")] if not skip_rust else [],
    datas=[
        (aw_qt_location / "resources/aw-qt.desktop", "aw_qt/resources"),
        (aw_qt_location / "media", "aw_qt/media"),
    ],
)
aw_server_a = build_analysis(
    "aw-server",
    aws_location,
    datas=[
        (aws_location / "aw_server/static", "aw_server/static"),
        (restx_path / "templates", "flask_restx/templates"),
        (restx_path / "static", "flask_restx/static"),
        (aw_core_path / "schemas", "aw_core/schemas"),
    ],
)
jcp_plus_pulp_capture_afk_a = build_analysis(
    "jcp_plus_pulp_capture_afk",
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
jcp_plus_pulp_capture_input_a = build_analysis("jcp_plus_pulp_capture_input", awi_location)
jcp_plus_pulp_capture_window_a = build_analysis(
    "jcp_plus_pulp_capture_window",
    aww_location,
    binaries=[
        (
            aww_location / "jcp_plus_pulp_capture_window/jcp-plus-pulp-capture-window-macos",
            "jcp_plus_pulp_capture_window",
        )
    ]
    if platform.system() == "Darwin"
    else [],
    datas=[
        (aww_location / "jcp_plus_pulp_capture_window/printAppStatus.jxa", "jcp_plus_pulp_capture_window")
    ],
)
jcp_plus_pulp_notify_a = build_analysis(
    "jcp_plus_pulp_notify", jcp_plus_pulp_notify_location, hiddenimports=["desktop_notifier.resources"]
)

# https://pythonhosted.org/PyInstaller/spec-files.html#multipackage-bundles
# MERGE takes a bit weird arguments, it wants tuples which consists of
# the analysis paired with the script name and the bin name
MERGE(
    (aw_server_a, "aw-server", "aw-server"),
    (aw_qt_a, "aw-qt", "aw-qt"),
    (jcp_plus_pulp_capture_afk_a, "jcp-plus-pulp-capture-afk", "jcp-plus-pulp-capture-afk"),
    (jcp_plus_pulp_capture_window_a, "jcp-plus-pulp-capture-window", "jcp-plus-pulp-capture-window"),
    (jcp_plus_pulp_capture_input_a, "jcp-plus-pulp-capture-input", "jcp-plus-pulp-capture-input"),
    (jcp_plus_pulp_notify_a, "jcp-plus-pulp-notify", "jcp-plus-pulp-notify"),
)


# aw-server
aws_coll = build_collect(aw_server_a, "aw-server")

# jcp-plus-pulp-capture-window
aww_coll = build_collect(jcp_plus_pulp_capture_window_a, "jcp-plus-pulp-capture-window")

# jcp-plus-pulp-capture-afk
awa_coll = build_collect(jcp_plus_pulp_capture_afk_a, "jcp-plus-pulp-capture-afk")

# aw-qt
awq_coll = build_collect(
    aw_qt_a,
    "aw-qt",
    console=False if platform.system() == "Windows" else True,
)

# jcp-plus-pulp-capture-input
awi_coll = build_collect(jcp_plus_pulp_capture_input_a, "jcp-plus-pulp-capture-input")

jcp_plus_pulp_notify_coll = build_collect(jcp_plus_pulp_notify_a, "jcp-plus-pulp-notify")

if platform.system() == "Darwin":
    app = BUNDLE(
        awq_coll,
        aws_coll,
        aww_coll,
        awa_coll,
        awi_coll,
        jcp_plus_pulp_notify_coll,
        name="ActivityWatch.app",
        icon=icon,
        bundle_identifier="net.activitywatch.ActivityWatch",
        version=current_release.lstrip("v"),
        info_plist={
            "NSPrincipalClass": "NSApplication",
            "CFBundleExecutable": "MacOS/aw-qt",
            "CFBundleIconFile": "logo.icns",
            "NSAppleEventsUsageDescription": "Please grant access to use Apple Events",
            # This could be set to a more specific version string (including the commit id, for example)
            "CFBundleVersion": current_release.lstrip("v"),
            # Replaced by the 'version' kwarg above
            # "CFBundleShortVersionString": current_release.lstrip('v'),
        },
    )
