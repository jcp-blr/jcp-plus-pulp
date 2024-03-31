.PHONY: build test package clean

build:
	poetry install

test:
	poetry run jcp-plus-pulp-capture-away --help  # Ensures that it at least starts
	make typecheck

typecheck:
	poetry run mypy jcp_plus_pulp_capture_away --ignore-missing-imports

package:
	pyinstaller jcp-plus-pulp-capture-away.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_capture_away/__pycache__
