.PHONY: build test benchmark typecheck typecheck-strict clean

build:
	poetry install

test:
	python -m pytest tests -v --cov=jcp_plus_pulp_core --cov=jcp_plus_pulp_datastore --cov=jcp_plus_pulp_transform --cov=jcp_plus_pulp_query

.coverage:
	make test

coverage_html: .coverage
	python -m coverage html -d coverage_html

benchmark:
	python -m jcp_plus_pulp_datastore.benchmark

typecheck:
	export MYPYPATH=./stubs; python -m mypy jcp_plus_pulp_core jcp_plus_pulp_datastore jcp_plus_pulp_transform jcp_plus_pulp_query --show-traceback --ignore-missing-imports --follow-imports=skip

typecheck-strict:
	export MYPYPATH=./stubs; python -m mypy jcp_plus_pulp_core jcp_plus_pulp_datastore jcp_plus_pulp_transform jcp_plus_pulp_query --strict-optional --check-untyped-defs; echo "Not a failing step"

PYFILES=$(shell find . -type f -name '*.py')
PYIFILES=$(shell find . -type f -name '*.pyi')

lint:
	ruff check .

lint-fix:
	pyupgrade --py37-plus ${PYFILES} && true
	ruff check --fix .

format:
	black ${PYFILES} ${PYIFILES}

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_core/__pycache__ jcp_plus_pulp_datastore/__pycache__
