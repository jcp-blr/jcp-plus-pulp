# -*- mode: python -*-
# vi: set ft=python :
import os

import jcp_plus_pulp_core
import flask_restx

jcp_plus_pulp_core_path = os.path.dirname(jcp_plus_pulp_core.__file__)
restx_path = os.path.dirname(flask_restx.__file__)

name = "jcp-plus-pulp-server"
block_cipher = None


a = Analysis(
    ["__main__.py"],
    pathex=[],
    binaries=None,
    datas=[
        (os.path.join(restx_path, "templates"), "flask_restx/templates"),
        (os.path.join(restx_path, "static"), "flask_restx/static"),
        (os.path.join(jcp_plus_pulp_core_path, "schemas"), "jcp_plus_pulp_core/schemas"),
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
    name=name,
    debug=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name="jcp-plus-pulp-server"
)
