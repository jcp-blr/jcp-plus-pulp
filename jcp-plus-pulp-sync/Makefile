.PHONY: build test package clean

build:
	poetry install
	# if macOS, build swift
	if [ "$(shell uname)" = "Darwin" ]; then \
		make build-swift; \
	fi

build-swift: jcp_plus_pulp_sync/jcp-plus-pulp-sync-macos

jcp_plus_pulp_sync/jcp-plus-pulp-sync-macos: jcp_plus_pulp_sync/macos.swift
	swiftc $^ -o $@

test:
	jcp-plus-pulp-sync --help

typecheck:
	poetry run mypy jcp_plus_pulp_sync/ --ignore-missing-imports

package:
	pyinstaller jcp-plus-pulp-sync.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_sync/__pycache__
	rm jcp_plus_pulp_sync/jcp-plus-pulp-sync-macos
