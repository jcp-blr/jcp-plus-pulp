.PHONY: build install test typecheck package clean

build:
	poetry install

install:
	cp misc/jcp-plus-pulp-server.service /usr/lib/systemd/user/jcp-plus-pulp-server.service

test:
	@# Note that extensive integration tests are also run in the bundle repo,
	@# for jcp-plus-pulp-server, but without code coverage.
	python -c 'import jcp_plus_pulp_server'
	python -m pytest tests/test_server.py

typecheck:
	python -m mypy jcp_plus_pulp_server tests --ignore-missing-imports

package:
	python -m jcp_plus_pulp_server.__about__
	rm -rf dist
	pyinstaller jcp-plus-pulp-server.spec --clean --noconfirm

PYFILES=$(shell find . -name '*.py')

lint:
	ruff check .

lint-fix:
	poetry run pyupgrade --py38-plus --exit-zero-even-if-changed $(PYFILES)
	ruff check --fix .

format:
	black .

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_server/__pycache__
	pip3 uninstall -y jcp_plus_pulp_server
