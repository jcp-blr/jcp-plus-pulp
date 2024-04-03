#!/bin/bash

# pick the latest zip
# NOTE: this assumes that the latest built zip is the only zip in the directory
ZIP_FILE=`ls ./dist/ -1 | grep zip | sort -r | head -1`
unzip ./dist/$ZIP_FILE

# fetch deps
wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-x86_64.AppImage
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# create AppRun
echo '#!/bin/sh
DIR="$(dirname "$(readlink -f "${0}")")"
"${DIR}"/jcp-plus-pulp-qt "$@"' > jcp-plus-pulp/AppRun
chmod a+x ./jcp-plus-pulp/AppRun

# build appimage
./linuxdeploy-x86_64.AppImage --appdir jcp-plus-pulp --executable ./jcp-plus-pulp/jcp-plus-pulp-qt --output appimage --desktop-file ./jcp-plus-pulp/jcp-plus-pulp-qt.desktop --icon-file ./jcp-plus-pulp/media/logo/logo.png --icon-filename jcp-plus-pulp
APPIMAGE_FILE=`ls -1 | grep AppImage| grep -i JCP+ PULP`
cp -v $APPIMAGE_FILE ./dist/jcp-plus-pulp-linux-x86_64.AppImage
