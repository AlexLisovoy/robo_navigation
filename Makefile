# Some useful commands (sorry, UNIX only).

.develop:
	pip install -U pip
	pip install -Ur requirements-dev.txt
	touch .develop

.install-deps:
	pip install -e .
	touch .install-deps

.clean-deps:
	@rm -rf .install-deps
	@rm -rf .develop

install: .clean-deps .develop .install-deps

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	python setup.py clean
	rm -rf .cache
	rm -f .coverage
	rm -rf coverage
	rm -rf .pytest_cache

flake: .develop .install-deps
	flake8 src tests

test: flake
	PYTHONPATH=`pwd` pytest -q tests

vtest: flake
	PYTHONPATH=`pwd` pytest -s -vv tests

cov cover coverage:
	PYTHONPATH=`pwd` pytest --cov=src  --cov-report=term --cov-report=html tests
	@echo "open file://`pwd`/coverage/index.html"

.PHONY: all install clean test vtest cov
