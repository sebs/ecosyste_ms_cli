.PHONY: setup clean test lint format prepare-release docker-build

PYTHON = python3.12
VENV = .venv
BIN = $(VENV)/bin

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e .[dev]
	$(BIN)/pip install pre-commit
	$(BIN)/pre-commit install --install-hooks



clean:
	$(BIN)/pre-commit uninstall
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

bandit:
	$(BIN)/bandit -r ./ecosystems_cli

black:
	$(BIN)/black ./ecosystems_cli
	$(BIN)/black ./tests

isort:
	$(BIN)/isort ./ecosystems_cli
	$(BIN)/isort ./tests

fix-all:
	$(BIN)/isort ./ecosystems_cli
	$(BIN)/isort ./tests
	$(BIN)/flake8 ./ecosystems_cli
	$(BIN)/flake8 ./tests
	$(BIN)/black ./ecosystems_cli
	$(BIN)/black ./tests

complexipy:
	$(BIN)/complexipy ./ecosystems_cli

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
	@echo "Preparing $(type) release..."
	$(BIN)/pip install commitizen
	$(BIN)/cz   bump --increment $(type)
	@current_version=$$(grep -o 'version = "[0-9]\+\.[0-9]\+\.[0-9]\+"' pyproject.toml | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+'); \
	echo "Version bumped to v$$current_version"; \
	git push origin main; \
	git push origin --tags; \
	echo "Release v$$current_version prepared and pushed!"; \
	echo "The GitHub Actions workflow will handle the release process."

docker-build:
	docker build -t ecosystems-cli:dev .
