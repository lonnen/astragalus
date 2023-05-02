DEFAULT_GOAL := help
PROJECT=astragalus

.PHONY: help
help:
	@echo "Available rules:"
	@fgrep -h "##" Makefile | fgrep -v fgrep | sed 's/\(.*\):.*##/\1:/'

.PHONY: clean
clean: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	find ${PROJECT} -name '*.pyc' -exec rm -f {} +
	find ${PROJECT} -name '*.pyo' -exec rm -f {} +
	find ${PROJECT} -name '*~' -exec rm -f {} +

.PHONY: lint
lint: ## Lint and black reformat files
	flake8 ${PROJECT} tests
	black --target-version=py37 ${PROJECT} tests

.PHONY: help
test: ## run tests with single local version of python
	py.test

.PHONY: help
test-all: ## run tests for all versions of python
	tox
