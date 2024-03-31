.PHONY: build test package clean

build:
	poetry install

test:
	poetry run jcp-plus-pulp-capture-afk --help  # Ensures that it at least starts
	make typecheck

typecheck:
	poetry run mypy jcp_plus_pulp_capture_afk --ignore-missing-imports

package:
	pyinstaller jcp-plus-pulp-capture-afk.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_capture_afk/__pycache__
