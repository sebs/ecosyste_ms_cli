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

bandit:
	$(BIN)/bandit -r ./ecosystems_cli

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
	$(BIN)/pip install bump2version
	$(BIN)/bump2version $(type) --tag --tag-message "Release {new_version}" --allow-dirty
	@current_version=$$(grep -o 'version="[0-9]\+\.[0-9]\+\.[0-9]\+"' setup.py | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+'); \
	echo "Version bumped to v$$current_version"; \
	echo ""; \
	date_now=$$(date +"%Y-%m-%d"); \
	if [ ! -f CHANGELOG.md ]; then \
		echo "# Changelog" > CHANGELOG.md; \
		echo "" >> CHANGELOG.md; \
	fi; \
	changelog_temp=$$(mktemp); \
	echo "# Changelog" > $$changelog_temp; \
	echo "" >> $$changelog_temp; \
	echo "## [v$$current_version] - $$date_now" >> $$changelog_temp; \
	echo "" >> $$changelog_temp; \
	prev_version=$$(git describe --abbrev=0 --tags HEAD^ 2>/dev/null || echo ""); \
	if [ -n "$$prev_version" ]; then \
		echo "### Changes since $$prev_version" >> $$changelog_temp; \
		echo "" >> $$changelog_temp; \
		git log $$prev_version..HEAD --pretty=format:"- %s" | grep -v "Merge" >> $$changelog_temp; \
		echo "" >> $$changelog_temp; \
		echo "" >> $$changelog_temp; \
	else \
		echo "### Initial release" >> $$changelog_temp; \
		echo "" >> $$changelog_temp; \
		git log --pretty=format:"- %s" | grep -v "Merge" >> $$changelog_temp; \
		echo "" >> $$changelog_temp; \
		echo "" >> $$changelog_temp; \
	fi; \
	if [ -f CHANGELOG.md ]; then \
		tail -n +3 CHANGELOG.md >> $$changelog_temp; \
	fi; \
	mv $$changelog_temp CHANGELOG.md; \
	git add CHANGELOG.md; \
	git commit -m "docs: update CHANGELOG for v$$current_version"; \
	git push origin main; \
	git push origin --tags; \
	echo "Release v$$current_version prepared and pushed!"; \
	echo "The GitHub Actions workflow will handle the release process."
