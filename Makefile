# =====================================
# Makefile for the JCP+ PULP bundle
# =====================================
#
# [GUIDE] How to install from source:
#
# We recommend creating and activating a Python virtualenv before building.
# Instructions on how to do this can be found in the guide linked above.
.PHONY: build install test clean clean_all

SHELL := /usr/bin/env bash

SUBMODULES := jcp-plus-pulp-core jcp-plus-pulp-client jcp-plus-pulp-qt jcp-plus-pulp-server jcp-plus-pulp-monitor-away jcp-plus-pulp-monitor-input jcp-plus-pulp-monitor-window jcp-plus-pulp-sync

# A function that checks if a target exists in a Makefile
# Usage: $(call has_target,<dir>,<target>)
define has_target
$(shell make -q -C $1 $2 >/dev/null 2>&1; if [ $$? -eq 0 -o $$? -eq 1 ]; then echo $1; fi)
endef

# Submodules with test/package/lint/typecheck targets
TESTABLES := $(foreach dir,$(SUBMODULES),$(call has_target,$(dir),test))
PACKAGEABLES := $(foreach dir,$(SUBMODULES),$(call has_target,$(dir),package))
LINTABLES := $(foreach dir,$(SUBMODULES),$(call has_target,$(dir),lint))
TYPECHECKABLES := $(foreach dir,$(SUBMODULES),$(call has_target,$(dir),typecheck))

# The `build` target
# ------------------
#
# What it does:
#  - Installs all the Python modules
#  - Builds the web UI and bundles it with jcp-plus-pulp-server
build:
#	needed due to https://github.com/pypa/setuptools/issues/1963
#	would ordinarily be specified in pyproject.toml, but is not respected due to https://github.com/pypa/setuptools/issues/1963
	pip install 'setuptools>49.1.1'
	for module in $(SUBMODULES); do \
		echo "Building $$module"; \
		make --directory=$$module build; \
	done
#   The below is needed due to: jcp-plus-pulp issue #173
	make --directory=jcp-plus-pulp-client build
	make --directory=jcp-plus-pulp-core build
#	Needed to ensure that the server has the correct version set
	python -c "import jcp_plus_pulp_server; print(jcp_plus_pulp_server.__version__)"

# Install
# -------
#
# Installs things like desktop/menu shortcuts.
# Might in the future configure autostart on the system.
install:
	make --directory=jcp-plus-pulp-qt install
# Installation is already happening in the `make build` step currently.
# We might want to change this.
# We should also add some option to install as user (pip3 install --user)

# Update
# ------
#
# Pulls the latest version, updates all the submodules, then runs `make build`.
update:
	git pull
	git submodule update --init --recursive
	make build

lint:
	@for module in $(LINTABLES); do \
		echo "Linting $$module"; \
		make --directory=$$module lint || { echo "Error in $$module lint"; exit 2; }; \
	done

typecheck:
	@for module in $(TYPECHECKABLES); do \
		echo "Typechecking $$module"; \
		make --directory=$$module typecheck || { echo "Error in $$module typecheck"; exit 2; }; \
	done

# Uninstall
# ---------
#
# Uninstalls all the Python modules.
uninstall:
	modules=$$(pip3 list --format=legacy | grep 'jcp-plus-pulp-' | grep -o '^jcp-plus-pulp-[^ ]*'); \
	for module in $$modules; do \
		echo "Uninstalling $$module"; \
		pip3 uninstall -y $$module; \
	done

test:
	@for module in $(TESTABLES); do \
		echo "Running tests for $$module"; \
		poetry run make -C $$module test || { echo "Error in $$module tests"; exit 2; }; \
    done

test-integration:
	# TODO: Move "integration tests" to jcp-plus-pulp-client
	# FIXME: For whatever reason the script stalls on Appveyor
	# jcp-plus-pulp-server-python
	@echo "== Integration testing jcp-plus-pulp-server =="
	@pytest ./scripts/tests/integration_tests.py ./jcp-plus-pulp-server/tests/ -v
	@pytest ./scripts/tests/integration_tests.py ./jcp-plus-pulp-server/tests/ -v

ICON := "jcp-plus-pulp-qt/media/logo/logo.png"

jcp-plus-pulp-qt/media/logo/logo.icns:
	mkdir -p build/MyIcon.iconset
	sips -z 16 16     $(ICON) --out build/MyIcon.iconset/icon_16x16.png
	sips -z 32 32     $(ICON) --out build/MyIcon.iconset/icon_16x16@2x.png
	sips -z 32 32     $(ICON) --out build/MyIcon.iconset/icon_32x32.png
	sips -z 64 64     $(ICON) --out build/MyIcon.iconset/icon_32x32@2x.png
	sips -z 128 128   $(ICON) --out build/MyIcon.iconset/icon_128x128.png
	sips -z 256 256   $(ICON) --out build/MyIcon.iconset/icon_128x128@2x.png
	sips -z 256 256   $(ICON) --out build/MyIcon.iconset/icon_256x256.png
	sips -z 512 512   $(ICON) --out build/MyIcon.iconset/icon_256x256@2x.png
	sips -z 512 512   $(ICON) --out build/MyIcon.iconset/icon_512x512.png
	cp				  $(ICON)       build/MyIcon.iconset/icon_512x512@2x.png
	iconutil -c icns build/MyIcon.iconset
	rm -R build/MyIcon.iconset
	mv build/MyIcon.icns jcp-plus-pulp-qt/media/logo/logo.icns

dist/JCP_PLUS_PULP.app: jcp-plus-pulp-qt/media/logo/logo.icns
	pyinstaller --clean --noconfirm jcp-plus-pulp.spec

dist/JCP_PLUS_PULP.dmg: dist/JCP+_PULP.app
	# NOTE: This does not codesign the dmg, that is done in the CI config
	pip install dmgbuild
	dmgbuild -s scripts/package/dmgbuild-settings.py -D app=dist/JCP+ PULP.app "JCP+ PULP" dist/JCP+ PULP.dmg

dist/notarize:
	./scripts/notarize.sh

package:
	rm -rf dist
	mkdir -p dist/jcp-plus-pulp
	for dir in $(PACKAGEABLES); do \
		make --directory=$$dir package; \
		cp -r $$dir/dist/$$dir dist/jcp-plus-pulp; \
	done
# Move jcp-plus-pulp-qt to the root of the dist folder
	mv dist/jcp-plus-pulp/jcp-plus-pulp-qt jcp-plus-pulp-qt-tmp
	mv jcp-plus-pulp-qt-tmp/* dist/jcp-plus-pulp
	rmdir jcp-plus-pulp-qt-tmp
# MG code below
	mv dist/jcp-plus-pulp/jcp-plus-pulp-monitor-away dist/jcp-plus-pulp/_internal/jcp-plus-pulp-monitor-away
	mv dist/jcp-plus-pulp/jcp-plus-pulp-monitor-input dist/jcp-plus-pulp/_internal/jcp-plus-pulp-monitor-input
	mv dist/jcp-plus-pulp/jcp-plus-pulp-monitor-window dist/jcp-plus-pulp/_internal/jcp-plus-pulp-monitor-window
	mv dist/jcp-plus-pulp/jcp-plus-pulp-server dist/jcp-plus-pulp/_internal/jcp-plus-pulp-server
	mv dist/jcp-plus-pulp/jcp-plus-pulp-sync dist/jcp-plus-pulp/_internal/jcp-plus-pulp-sync
# Remove problem-causing binaries
	rm -f dist/jcp-plus-pulp/libdrm.so.2       # see: jcp-plus-pulp issue #161
	rm -f dist/jcp-plus-pulp/libharfbuzz.so.0  # see: jcp-plus-pulp issue #660#issuecomment-959889230
# These should be provided by the distro itself
# Had to be removed due to otherwise causing the error:
	rm -f dist/jcp-plus-pulp/libfontconfig.so.1
	rm -f dist/jcp-plus-pulp/libfreetype.so.6
# Remove unnecessary files
	rm -rf dist/jcp-plus-pulp/pytz
# Builds zips and setups
	bash scripts/package/package-all.sh

clean:
	rm -rf build dist

# Clean all subprojects
clean_all: clean
	for dir in $(SUBMODULES); do \
		make --directory=$$dir clean; \
	done

clean-auto:
	rm -rIv **/jcp-plus-pulp-android/mobile/build
	rm -rIfv **/node_modules
