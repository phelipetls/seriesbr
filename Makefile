SHELL=/bin/bash

PACKAGE = seriesbr
TEST_DIR = tests

test:
	pytest

clean:
	rm -rf build dist .egg $(PACKAGE).egg-info
	coverage erase

publish:
	python3 setup.py sdist bdist_wheel
	twine upload --skip-existing dist/*
	rm -rf build dist .egg $(PACKAGE).egg-info

publish-test:
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	rm -rf build dist .egg $(PACKAGE).egg-info

lint:
	flake8 $(PACKAGE)

COVERAGE = pytest --cov=$(PACKAGE) tests
CLEAR_COVERAGE = coverage erase

cov:
	$(COVERAGE)
	$(CLEAR_COVERAGE)

htmlcov:
	$(COVERAGE)
	coverage html
	$(CLEAR_COVERAGE)
	firefox htmlcov/index.html

fix:
	nvim -q <(flake8 --exclude=venv* .)

PROFILE_SCRIPT = profiler.py
PROFILE_OUTPUT = profile.txt

profile:
	python3 -m cProfile -o $(PROFILE_OUTPUT) -s cumtime $(PROFILE_SCRIPT)

.PHONY: test publish lint cov fix htmlcov profile
