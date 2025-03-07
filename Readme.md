# Ecosystems CLI

A command-line interface for interacting with ecosyste.ms APIs.

## Installation

Requirements:
- Python 3.12+

```bash
# Clone the repository
git clone https://github.com/yourusername/ecosyste_ms_cli.git
cd ecosyste_ms_cli

# Set up virtual environment and install dependencies
make setup

# Activate virtual environment
source .venv/bin/activate

# Install in development mode
pip install -e .
```

## Usage

Each command includes helpful examples in its help text. Use `--help` with any command to see usage examples.

```bash
# Show available commands
ecosystems --help
```

### Repos API

```bash
# List all topics
ecosystems repos topics

# Get a specific topic
ecosystems repos topic javascript

# List all repository hosts
ecosystems repos hosts

# Get a specific host
ecosystems repos host GitHub

# Get a specific repository
ecosystems repos repository GitHub facebook react
```

### Packages API

```bash
# List all registries
ecosystems packages registries

# Get a specific registry
ecosystems packages registry npm

# Get a specific package
ecosystems packages package npm express

# Get a specific package version
ecosystems packages version npm express 4.17.1
```

### Summary API

```bash
# Get repository summary
ecosystems summary repo https://github.com/facebook/react

# Get package summary
ecosystems summary package https://www.npmjs.com/package/express
```

### Advanced Usage

#### API Operation Calls

You can call any API operation directly:

```bash
# Call an operation with parameters
ecosystems repos call topic --path-params '{"topic": "javascript"}'
ecosystems repos call topics --query-params '{"sort": "repositories_count"}'
ecosystems packages call getRegistry --path-params '{"name": "npm"}'
ecosystems summary call getRepositorySummary --query-params '{"url": "https://github.com/facebook/react"}'
```

#### List Available Operations

```bash
# List operations for a specific API
ecosystems packages list
ecosystems repos list
ecosystems summary list
```

## Development

```bash
# Run tests
make test

# Run linting
make lint

# Format code
make format

# Clean up
make clean
```

## API Structure

The CLI provides access to three ecosyste.ms APIs:

1. **packages** - Package registry data
2. **repos** - Repository data
3. **summary** - Summary data

Each API has its own set of operations that can be accessed through convenience commands or the generic `call` command.

