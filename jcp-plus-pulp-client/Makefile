.PHONY: build test typecheck clean examples

build:
	poetry install

test-integration:
	pytest -v tests/test_client.py

typecheck:
	poetry run mypy

PYFILES=jcp_plus_pulp_client/*.py examples/*.py

lint:
	ruff check .

lint-fix:
	pyupgrade --py38-plus ${PYFILES} --exit-zero-even-if-changed
	ruff check --fix .

format:
	black .

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_client/__pycache__
