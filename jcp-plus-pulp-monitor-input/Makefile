.PHONY: build test package clean

build:
	poetry install

test:
	poetry run jcp-plus-pulp-monitor-input --help  # Ensures that it at least starts
	make typecheck

typecheck:
	poetry run mypy src/jcp_plus_pulp_monitor_input --ignore-missing-imports

package:
	pyinstaller jcp-plus-pulp-monitor-input.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_monitor_input/__pycache__
