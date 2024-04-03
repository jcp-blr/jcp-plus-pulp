.PHONY: build test package clean

build:
	poetry install

test:
	poetry run jcp-plus-pulp-monitor-away --help  # Ensures that it at least starts
	make typecheck

typecheck:
	poetry run mypy jcp_plus_pulp_monitor_away --ignore-missing-imports

package:
	pyinstaller jcp-plus-pulp-monitor-away.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_monitor_away/__pycache__
