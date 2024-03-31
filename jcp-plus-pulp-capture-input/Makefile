.PHONY: build test package clean

build:
	poetry install

test:
	poetry run jcp-plus-pulp-capture-input --help  # Ensures that it at least starts
	make typecheck

typecheck:
	poetry run mypy src/jcp_plus_pulp_capture_input --ignore-missing-imports

build-vis:
	#npm install -g pug-cli browserify
	cd visualization && make build

package:
	pyinstaller jcp-plus-pulp-capture-input.spec --clean --noconfirm
	# if dist/visualization/dist exists, include in package
	if [ -d "visualization/dist" ]; then \
		mkdir -p dist/visualization; \
		cp -r visualization/dist/* dist/visualization; \
	fi

clean:
	rm -rf build dist
	rm -rf jcp_plus_pulp_capture_input/__pycache__
