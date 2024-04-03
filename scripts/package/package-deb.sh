#!/usr/bin/bash
# Setting the shell is required, as `sh` doesn't support slicing.

# Fail fast
set -e
# Verbose commands for CI verification
set -x

VERSION=$(scripts/package/getversion.sh)
# Slice off the "v" from the tag, which is probably guaranteed
VERSION_NUM=${VERSION:1}
echo $VERSION_NUM
PKGDIR="jcp_plus_pulp_$VERSION_NUM"

# Package tools
sudo apt-get install sed jdupes wget

if [ -d "PKGDIR" ]; then
    sudo rm -rf $PKGDIR
fi

# .deb meta files
mkdir -p $PKGDIR/DEBIAN
# jcp-plus-pulp's install location
mkdir -p $PKGDIR/opt
# Allows jcp-plus-pulp-qt to autostart.
mkdir -p $PKGDIR/etc/xdg/autostart
# Allows users to manually start jcp-plus-pulp-qt from their start menu.
mkdir -p $PKGDIR/usr/share/applications

# While storing the control file in a variable here, dumping it in a file is so unnecessarily
# complicated that it's easier to just dump move and sed.
cp ./scripts/package/deb/control $PKGDIR/DEBIAN/control
sed -i "s/SCRIPT_VERSION_HERE/${VERSION_NUM}/" $PKGDIR/DEBIAN/control

# Verify the file content
cat $PKGDIR/DEBIAN/control
# The entire opt directory (should) consist of dist/jcp-plus-pulp/*

cp -r dist/jcp-plus-pulp/ $PKGDIR/opt/

# Hard link duplicated libraries
# (I have no idea what this is for)
jdupes -L -r -S -Xsize-:1K $PKGDIR/opt/

sudo chown -R root:root $PKGDIR

# Prepare the .desktop file
sudo sed -i 's!Exec=jcp-plus-pulp-qt!Exec=/opt/jcp-plus-pulp/jcp-plus-pulp-qt!' $PKGDIR/opt/jcp-plus-pulp/jcp-plus-pulp-qt.desktop
sudo cp $PKGDIR/opt/jcp-plus-pulp/jcp-plus-pulp-qt.desktop $PKGDIR/etc/xdg/autostart/
sudo cp $PKGDIR/opt/jcp-plus-pulp/jcp-plus-pulp-qt.desktop $PKGDIR/usr/share/applications/

dpkg-deb --build $PKGDIR
sudo mv jcp_plus_pulp_${VERSION_NUM}.deb dist/jcp-plus-pulp-${VERSION}-linux-x86_64.deb
