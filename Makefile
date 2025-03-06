.PHONY: setup venv dependencies clean test lint format help

# Global variables
PYTHON := python3.12
VENV_DIR := .venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip

# Default target
help:
	@echo "Available targets:"
	@echo "  setup           - Set up the complete project environment"
	@echo "  venv            - Create virtual environment"
	@echo "  dependencies    - Install dependencies"
	@echo "  clean           - Remove virtual environment and cache files"
	@echo "  test            - Run tests"
	@echo "  lint            - Run linting checks"
	@echo "  format          - Format code using black and isort"

# Complete setup
setup: venv dependencies
	@echo "Project setup complete. Activate the virtual environment with:"
	@echo "source $(VENV_DIR)/bin/activate"

# Virtual environment
venv:
	@echo "Creating virtual environment with Python $(PYTHON)..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip

# Dependencies
dependencies: venv
	@echo "Installing dependencies..."
	@$(VENV_BIN)/pip install -r requirements.txt
	@$(VENV_BIN)/pip install -e .

# Clean project
clean:
	@echo "Cleaning project..."
	@rm -rf $(VENV_DIR) __pycache__ *.egg-info dist build .pytest_cache .coverage

# Test
test: venv
	@echo "Running tests..."
	@$(VENV_BIN)/pytest

# Lint
lint: venv
	@echo "Running linting..."
	@$(VENV_BIN)/flake8 ecosyste_ms_cli
	@$(VENV_BIN)/mypy ecosyste_ms_cli

# Format
format: venv
	@echo "Formatting code..."
	@$(VENV_BIN)/black ecosyste_ms_cli
	@$(VENV_BIN)/isort ecosyste_ms_cli

# Generate API clients
generate-clients:
	@echo "Creating clients directory structure..."
	@mkdir -p ./ecosyste_ms_cli/clients/repos
	@mkdir -p ./ecosyste_ms_cli/clients/packages
	@mkdir -p ./ecosyste_ms_cli/clients/summary
	@touch ./ecosyste_ms_cli/clients/repos/__init__.py
	@touch ./ecosyste_ms_cli/clients/packages/__init__.py
	@touch ./ecosyste_ms_cli/clients/summary/__init__.py
	@echo "Basic client structure created. API clients are assumed to be in place."
	@echo "Note: To generate actual API clients from OpenAPI specs, use 'make generate-openapi-clients'"

# Generate OpenAPI clients
generate-openapi-clients: generate-repos-client-openapi generate-packages-client-openapi generate-summary-client-openapi
	@echo "All OpenAPI clients generated successfully (if no errors occurred)."

# Generate Repos API client from OpenAPI
generate-repos-client-openapi:
	@echo "Generating Repos API client from OpenAPI spec..."
	@mkdir -p ./generated-clients
	@CID=$$(docker run -d -v "$(PWD)/apis:/local/apis" -p 8888:8080 openapitools/openapi-generator-online) && \
	sleep 10 && \
	RESPONSE=$$(curl -s -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' \
	-d '{"openAPIUrl": "file:///local/apis/repos.openapi.yaml", "options": {"packageName": "ecosyste_ms_cli.clients.repos", "projectName": "ecosystems-repos-client"}}' \
	'http://localhost:8888/api/gen/clients/python') && \
	echo "OpenAPI Response: $$RESPONSE" && \
	LINK=$$(echo $$RESPONSE | grep -o '"link":"[^"]*"' | sed 's/"link":"\(.*\)"/\1/') && \
	echo "Download Link: $$LINK" && \
	wget -q $$LINK -O repos-client.zip && \
	mkdir -p ./generated-clients/repos && \
	unzip -o repos-client.zip -d ./generated-clients/repos && \
	rm -rf repos-client.zip && \
	docker stop $$CID && docker rm $$CID
	@echo "Repos API client generation completed. Client available in ./generated-clients/repos"

# Generate Packages API client from OpenAPI
generate-packages-client-openapi:
	@echo "Generating Packages API client from OpenAPI spec..."
	@mkdir -p ./generated-clients
	@CID=$$(docker run -d -v "$(PWD)/apis:/local/apis" -p 8888:8080 openapitools/openapi-generator-online) && \
	sleep 10 && \
	RESPONSE=$$(curl -s -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' \
	-d '{"openAPIUrl": "file:///local/apis/packages.openapi.yaml", "options": {"packageName": "ecosyste_ms_cli.clients.packages", "projectName": "ecosystems-packages-client"}}' \
	'http://localhost:8888/api/gen/clients/python') && \
	echo "OpenAPI Response: $$RESPONSE" && \
	LINK=$$(echo $$RESPONSE | grep -o '"link":"[^"]*"' | sed 's/"link":"\(.*\)"/\1/') && \
	echo "Download Link: $$LINK" && \
	wget -q $$LINK -O packages-client.zip && \
	mkdir -p ./generated-clients/packages && \
	unzip -o packages-client.zip -d ./generated-clients/packages && \
	rm -rf packages-client.zip && \
	docker stop $$CID && docker rm $$CID
	@echo "Packages API client generation completed. Client available in ./generated-clients/packages"

# Generate Summary API client from OpenAPI
generate-summary-client-openapi:
	@echo "Generating Summary API client from OpenAPI spec..."
	@mkdir -p ./generated-clients
	@CID=$$(docker run -d -v "$(PWD)/apis:/local/apis" -p 8888:8080 openapitools/openapi-generator-online) && \
	sleep 10 && \
	RESPONSE=$$(curl -s -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' \
	-d '{"openAPIUrl": "file:///local/apis/summary.openapi.yaml", "options": {"packageName": "ecosyste_ms_cli.clients.summary", "projectName": "ecosystems-summary-client"}}' \
	'http://localhost:8888/api/gen/clients/python') && \
	echo "OpenAPI Response: $$RESPONSE" && \
	LINK=$$(echo $$RESPONSE | grep -o '"link":"[^"]*"' | sed 's/"link":"\(.*\)"/\1/') && \
	echo "Download Link: $$LINK" && \
	wget -q $$LINK -O summary-client.zip && \
	mkdir -p ./generated-clients/summary && \
	unzip -o summary-client.zip -d ./generated-clients/summary && \
	rm -rf summary-client.zip && \
	docker stop $$CID && docker rm $$CID
	@echo "Summary API client generation completed. Client available in ./generated-clients/summary"

# Create empty API clients
create-empty-clients:
	@echo "Creating empty API client directories..."
	@mkdir -p ./ecosyste_ms_cli/clients/repos
	@mkdir -p ./ecosyste_ms_cli/clients/packages
	@mkdir -p ./ecosyste_ms_cli/clients/summary
	@touch ./ecosyste_ms_cli/clients/repos/__init__.py
	@touch ./ecosyste_ms_cli/clients/packages/__init__.py
	@touch ./ecosyste_ms_cli/clients/summary/__init__.py
	@echo "Empty API client directories created. Use them to implement client functionality."
