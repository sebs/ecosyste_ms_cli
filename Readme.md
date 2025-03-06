# Ecosyste.ms CLI

The Ecosyste.ms CLI is a command-line tool for interacting with the [Ecosyste.ms](https://ecosyste.ms) APIs. It provides a simple and powerful interface to query and manipulate data from various Ecosyste.ms services.

## Features

- Python 3.12 compatible
- Built with [Typer](https://typer.tiangolo.com/) for a clean CLI interface
- Support for multiple Ecosyste.ms APIs:
  - Repositories API
  - Packages API
  - Summary API
- Output in multiple formats (JSON, TSV, CSV)
- Command completion for ease of use
- Comprehensive documentation and examples

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

### Setup with Make

The project includes a Makefile to simplify the setup process:

```bash
# Clone the repository
git clone https://github.com/ecosyste-ms/cli.git
cd cli

# Set up the project (creates virtual environment and installs dependencies)
make setup

# Activate the virtual environment
source .venv/bin/activate
```

### Manual Setup

If you prefer to set up the project manually:

```bash
# Clone the repository
git clone https://github.com/ecosyste-ms/cli.git
cd cli

# Create a virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Usage

After installation, you can use the `ecosystems` command to interact with Ecosyste.ms APIs:

```bash
# Get help
ecosystems --help

# List available topics
ecosystems topics --list

# Get repositories for a specific topic
ecosystems topics --topic <topic-name>
```

## Development

### Project Structure

```
ecosyste_ms_cli/
├── clients/        # Generated API clients
├── commands/       # Command implementations
├── utils/          # Utility functions
└── main.py         # CLI entry point
```

### Development Tools

The project uses the following development tools:

- `pytest` for testing
- `black` and `isort` for code formatting
- `flake8` for linting
- `mypy` for type checking

You can run these tools using the Makefile:

```bash
# Run tests
make test

# Format code
make format

# Run linting
make lint
```

### Makefile Reference

The project includes a comprehensive Makefile to streamline development tasks:

| Target | Description |
|--------|-------------|
| `setup` | Complete project setup (venv + dependencies) |
| `venv` | Create virtual environment |
| `dependencies` | Install all project dependencies including API client wheels |
| `clean` | Remove build artifacts and temporary files |
| `test` | Run test suite |
| `lint` | Run linting checks |
| `format` | Auto-format code with black and isort |
| `generate-openapi-clients` | Generate API clients from OpenAPI specs |
| `build-client-wheels` | Build wheels for all API clients |
| `build-wheel` | Build wheel for main project |
| `ensure-client-wheels` | Check if clients exist and build wheels if needed |

## License

MIT

