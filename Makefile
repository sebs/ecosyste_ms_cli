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
	@echo "Preparing $(type) release..."
	@current_version=$$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0"); \
	current_version=$${current_version#v}; \
	major=$$(echo $$current_version | cut -d. -f1); \
	minor=$$(echo $$current_version | cut -d. -f2); \
	patch=$$(echo $$current_version | cut -d. -f3); \
	if [ "$(type)" = "major" ]; then \
		next_version=$$((major + 1)).0.0; \
	elif [ "$(type)" = "minor" ]; then \
		next_version=$$major.$$((minor + 1)).0; \
	else \
		next_version=$$major.$$minor.$$((patch + 1)); \
	fi; \
	echo "Current version: $$current_version"; \
	echo "Next version: $$next_version"; \
	echo ""; \
	# Update version in setup.py \
	sed -i.bak "s/version=\"[0-9]\+\.[0-9]\+\.[0-9]\+\"/version=\"$$next_version\"/" setup.py; \
	rm -f setup.py.bak; \
	echo "Updated version in setup.py to $$next_version"; \
	echo ""; \
	date_now=$$(date +"%Y-%m-%d"); \
	if [ ! -f CHANGELOG.md ]; then \
		echo "# Changelog" > CHANGELOG.md; \
		echo "" >> CHANGELOG.md; \
	fi; \
	changelog_temp=$$(mktemp); \
	echo "# Changelog" > $$changelog_temp; \
	echo "" >> $$changelog_temp; \
	echo "## [v$$next_version] - $$date_now" >> $$changelog_temp; \
	echo "" >> $$changelog_temp; \
	if [ "$$current_version" != "0.0.0" ]; then \
		echo "### Changes since v$$current_version" >> $$changelog_temp; \
		echo "" >> $$changelog_temp; \
		git log v$$current_version..HEAD --pretty=format:"- %s" | grep -v "Merge" >> $$changelog_temp; \
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
	git add setup.py CHANGELOG.md; \
	git commit -m "Update version to v$$next_version and update CHANGELOG"; \
	git tag -a "v$$next_version" -m "Release v$$next_version"; \
	git push origin main; \
	git push origin v$$next_version; \
	echo ""; \
	echo "Release v$$next_version prepared and pushed!"; \
	echo "The GitHub Actions workflow will handle the release process."
