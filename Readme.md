# Ecosystems CLI

A command-line interface for interacting with ecosyste.ms APIs.

## Setup

Requirements:
- Python 3.12

```bash
# Set up virtual environment and install dependencies
make setup

# Activate virtual environment
source .venv/bin/activate
```

## Usage

```bash
# Show available commands
ecosystems --help

# List operations for a specific API
ecosystems packages list
ecosystems repos list
ecosystems summary list

# Call an API operation (using JSON parameters)
ecosystems repos call topic --path-params '{"topic": "ux"}'
ecosystems packages call getRegistries

# Use convenience commands for common operations

## Repos API

```bash
# List all topics
ecosystems repos topics
# Example output: [{"name": "javascript", "repositories_count": 12345}, ...]

# Get a specific topic
ecosystems repos topic javascript
# Example output: {"name": "javascript", "repositories_count": 12345, ...}

# List all repository hosts
ecosystems repos hosts
# Example output: [{"name": "GitHub", "url": "https://github.com", ...}, ...]

# Get a specific host
ecosystems repos host GitHub
# Example output: {"name": "GitHub", "url": "https://github.com", ...}

# Get a specific repository
ecosystems repos repository GitHub facebook react
# Example output: {"full_name": "facebook/react", "description": "A JavaScript library for building user interfaces", ...}
```

## Packages API

```bash
# List all registries
ecosystems packages registries
# Example output: [{"name": "npm", "url": "https://www.npmjs.com", ...}, ...]

# Get a specific registry
ecosystems packages registry npm
# Example output: {"name": "npm", "url": "https://www.npmjs.com", ...}

# Get a specific package
ecosystems packages package npm express
# Example output: {"name": "express", "description": "Fast, unopinionated, minimalist web framework", ...}

# Get a specific package version
ecosystems packages version npm express 4.17.1
# Example output: {"version": "4.17.1", "licenses": "MIT", ...}
```

## Summary API

```bash
# Get repository summary
ecosystems summary repo https://github.com/facebook/react
# Example output: {"url": "https://github.com/facebook/react", "stars": 123456, ...}

# Get package summary
ecosystems summary package https://www.npmjs.com/package/express
# Example output: {"url": "https://www.npmjs.com/package/express", "downloads": 1234567, ...}
```

## Direct Parameter Access (no JSON required)

```bash
# Get a specific topic using direct parameter access
ecosystems op repos topic ux
# Example output: {"name": "ux", "repositories_count": 5678, ...}

# Get a specific registry using direct parameter access
ecosystems op packages getRegistry npm
# Example output: {"name": "npm", "url": "https://www.npmjs.com", ...}

# Get a repository with direct parameter access
ecosystems op repos getHostRepository GitHub facebook/react
# Example output: {"full_name": "facebook/react", "description": "A JavaScript library for building user interfaces", ...}
```


### API Structure

The CLI provides access to three ecosyste.ms APIs:

1. **packages** - Package registry data
2. **repos** - Repository data
3. **summary** - Summary data

Each API has two main commands:
- `list` - Lists all available operations
- `call` - Calls a specific operation with parameters

### Parameters

When calling an operation, you can provide the following parameters:

```bash
# Using path parameters
ecosystems repos call topic --path-params '{"topic": "javascript"}'
# Example output: {"name": "javascript", "repositories_count": 12345, ...}

# Using query parameters
ecosystems repos call topics --query-params '{"sort": "repositories_count"}'
# Example output: [{"name": "javascript", "repositories_count": 12345}, ...]

# Using body parameters (for POST requests)
ecosystems repos call somePostOperation --body '{"name": "value"}'
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
