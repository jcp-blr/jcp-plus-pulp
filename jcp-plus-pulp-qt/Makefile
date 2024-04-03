.PHONY: build install test test-integration typecheck package clean

build:
	poetry install

install:
	bash scripts/config-autostart.sh

test:
	python -c 'import jcp_plus_pulp_qt'

test-integration:
	python ./tests/integration_tests.py --no-modules

lint:
	poetry run flake8 jcp_plus_pulp_qt --ignore=E501,E302,E305,E231 --per-file-ignores="__init__.py:F401"

typecheck:
	poetry run mypy jcp_plus_pulp_qt --pretty

precommit:
	make typecheck
	make test
	make test-integration

package:
	pyinstaller --clean --noconfirm jcp-plus-pulp-qt.spec

clean:
	rm -rf build dist
	rm -rf __pycache__ jcp_plus_pulp_qt/__pycache__

#jcp_plus_pulp_qt/resources.py: jcp_plus_pulp_qt/resources.qrc
#	poetry run pyrcc5 -o jcp_plus_pulp_qt/resources.py jcp_plus_pulp_qt/resources.qrc
