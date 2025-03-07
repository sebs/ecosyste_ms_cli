.PHONY: setup clean test lint format prepare-release

PYTHON = python3.12
VENV = .venv
BIN = $(VENV)/bin

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e .[dev]

clean:
	rm -rf $(VENV)
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

test:
	$(BIN)/pytest

lint:
	$(BIN)/flake8
	$(BIN)/black --check .
	$(BIN)/isort --check .

format:
	$(BIN)/black .
	$(BIN)/isort .

prepare-release:
	@if [ "$(type)" != "major" ] && [ "$(type)" != "minor" ] && [ "$(type)" != "patch" ]; then \
		echo "Error: type parameter must be 'major', 'minor', or 'patch'"; \
		echo "Usage: make prepare-release type=<major|minor|patch>"; \
		exit 1; \
	fi
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Error: Working directory is not clean. Please commit or stash your changes first."; \
		git status; \
		exit 1; \
	fi
	@echo "Preparing $(type) release using semantic-release..."
	$(BIN)/pip install python-semantic-release build
	$(BIN)/semantic-release version --$(type)
	echo "Release prepared! The GitHub Actions workflow will handle the release process."
