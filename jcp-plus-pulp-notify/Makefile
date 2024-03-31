.PHONY: build test package clean

build:
	poetry install

test:
	poetry run jcp-plus-pulp-notify --help  # Ensures that it at least starts
	make typecheck

typecheck:
	poetry run mypy jcp_plus_pulp_notify --ignore-missing-imports

package:
	pyinstaller jcp-plus-pulp-notify.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_notify/__pycache__
