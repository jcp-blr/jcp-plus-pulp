.PHONY: build test package clean

build:
	poetry install
	# if macOS, build swift
	if [ "$(shell uname)" = "Darwin" ]; then \
		make build-swift; \
	fi

build-swift: jcp_plus_pulp_monitor_window/jcp-plus-pulp-monitor-window-macos

jcp_plus_pulp_monitor_window/jcp-plus-pulp-monitor-window-macos: jcp_plus_pulp_monitor_window/macos.swift
	swiftc $^ -o $@

test:
	jcp-plus-pulp-monitor-window --help

typecheck:
	poetry run mypy jcp_plus_pulp_monitor_window/ --ignore-missing-imports

package:
	pyinstaller jcp-plus-pulp-monitor-window.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_monitor_window/__pycache__
	rm jcp_plus_pulp_monitor_window/jcp-plus-pulp-monitor-window-macos
