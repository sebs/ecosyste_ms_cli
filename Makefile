.PHONY: setup venv dependencies clean test lint format help generate-openapi-clients

# Global variables
PYTHON := python3.12
VENV_DIR := .venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip
GENERATED_DIR := ./generated-clients
OPENAPI_IMAGE := openapitools/openapi-generator-online
OPENAPI_PORT := 8888
API_SERVICES := repos packages summary

# Default target
help:
	@echo "Available targets:"
	@echo "  setup                     - Set up the complete project environment"
	@echo "  venv                      - Create virtual environment"
	@echo "  dependencies              - Install dependencies"
	@echo "  clean                     - Remove virtual environment and cache files"
	@echo "  test                      - Run tests"
	@echo "  lint                      - Run linting checks"
	@echo "  format                    - Format code using black and isort"
	@echo "  generate-openapi-clients  - Generate OpenAPI clients for all services"

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
dependencies: venv ensure-client-wheels
	@echo "Installing dependencies..."
	@$(VENV_BIN)/pip install -r requirements.txt
	@echo "Installing client wheels..."
	@$(VENV_BIN)/pip install -r requirements-wheels.txt
	@echo "Installing project..."
	@$(VENV_BIN)/pip install --use-pep517 .

# Ensure client wheels exist
ensure-client-wheels:
	@echo "Checking for OpenAPI clients..."
	@if [ ! -d "$(GENERATED_DIR)/repos/python-client" ] || \
	   [ ! -d "$(GENERATED_DIR)/packages/python-client" ] || \
	   [ ! -d "$(GENERATED_DIR)/summary/python-client" ]; then \
		echo "Generating missing API clients first..."; \
		$(MAKE) generate-openapi-clients; \
	fi
	@echo "Checking for client wheels..."
	@if [ ! -f "$(GENERATED_DIR)/repos/python-client/dist/ecosystems_repos_client-1.0.0-py2.py3-none-any.whl" ] || \
	   [ ! -f "$(GENERATED_DIR)/packages/python-client/dist/ecosystems_packages_client-1.0.0-py2.py3-none-any.whl" ] || \
	   [ ! -f "$(GENERATED_DIR)/summary/python-client/dist/ecosystems_summary_client-1.0.0-py2.py3-none-any.whl" ]; then \
		echo "Building missing client wheels..."; \
		$(MAKE) build-client-wheels; \
	else \
		echo "All client wheels already exist."; \
	fi

# Clean project
clean:
	@echo "Cleaning project..."
	@rm -rf __pycache__ *.egg-info dist build wheels .pytest_cache .coverage $(GENERATED_DIR)

# Build wheel for the main project
build-wheel:
	@echo "Building wheel for main project..."
	@$(VENV_BIN)/python -m pip install --upgrade build wheel
	@$(VENV_BIN)/python -m build --wheel
	@echo "Wheel built successfully in dist/ directory"

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

# Generate OpenAPI clients for all services
generate-openapi-clients: $(addprefix generate-client-,$(API_SERVICES))
	@echo "All OpenAPI clients generated successfully (if no errors occurred)."

# Define a pattern rule for generating clients
generate-client-%:
	@echo "Generating $* API client from OpenAPI spec..."
	@mkdir -p $(GENERATED_DIR)/$*
	@CID=$$(docker run -d -v "$(PWD)/apis:/local/apis" -p $(OPENAPI_PORT):8080 $(OPENAPI_IMAGE)) && \
	sleep 10 && \
	RESPONSE=$$(curl -s -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' \
	-d '{"openAPIUrl": "file:///local/apis/$*.openapi.yaml", "options": {"packageName": "ecosyste_ms_cli.clients.$*", "projectName": "ecosystems-$*-client"}}' \
	'http://localhost:$(OPENAPI_PORT)/api/gen/clients/python') && \
	echo "OpenAPI Response: $$RESPONSE" && \
	LINK=$$(echo $$RESPONSE | grep -o '"link":"[^"]*"' | sed 's/"link":"\(.*\)"/\1/') && \
	echo "Download Link: $$LINK" && \
	wget -q $$LINK -O $*-client.zip && \
	mkdir -p $(GENERATED_DIR)/$* && \
	unzip -o $*-client.zip -d $(GENERATED_DIR)/$* && \
	rm -rf $*-client.zip && \
	docker stop $$CID && docker rm $$CID
	@echo "$* API client generation completed. Client available in $(GENERATED_DIR)/$*"


# Create universal wheel setup.cfg file
create-wheel-config:
	@echo '[bdist_wheel]' > wheel-setup.cfg
	@echo 'universal=1' >> wheel-setup.cfg

# Build wheels for all generated clients
build-client-wheels: create-wheel-config
	@echo "Building wheels for all API clients..."
	@for service in $(API_SERVICES); do \
		echo "Building wheel for $$service client..."; \
		cp wheel-setup.cfg $(GENERATED_DIR)/$$service/python-client/setup.cfg; \
		cd $(GENERATED_DIR)/$$service/python-client && \
		python -m pip install --upgrade build wheel && \
		python -m build --wheel && \
		cd - > /dev/null; \
	done
	@rm wheel-setup.cfg
	@echo "All client wheels built successfully (universal wheels compatible with Python 2 and 3)"