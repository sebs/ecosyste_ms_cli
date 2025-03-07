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

### Global Options

- `--timeout`: Set the timeout in seconds for all HTTP requests (default: 20 seconds)
- `--format`: Set the output format (default: table). Available formats: table, json, tsv, jsonl

```bash
# Example: Set a 30-second timeout for all requests
ecosystems --timeout 30 repos topics

# Example: Get output in JSON format
ecosystems --format json repos topics

# Example: Get output in TSV format (tab-separated values)
ecosystems --format tsv repos topics

# Example: Get output in JSONL format (JSON Lines)
ecosystems --format jsonl repos topics
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

### Awesome API

```bash
# List all projects
ecosystems awesome projects

# Get a specific project by ID
ecosystems awesome project 123456

# List all lists
ecosystems awesome lists

# Get a specific list by ID
ecosystems awesome list 123

# Get projects in a specific list
ecosystems awesome list-projects 123

# List all topics
ecosystems awesome topics

# Get a specific topic by slug
ecosystems awesome topic javascript
```

### Advanced Usage

#### API Operation Calls

#### List Available Operations

```bash
# List operations for a specific API
ecosystems packages list
ecosystems repos list
ecosystems summary list
ecosystems awesome operations
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

### Conventional Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for standardized commit messages. The format helps maintain a readable history and automates versioning and changelog generation.

Commit messages should follow this pattern:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Common types include:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or modifying tests
- `chore`: Changes to the build process or auxiliary tools

Example: `feat(cli): add examples to command help text`

## API Structure

The CLI provides access to three ecosyste.ms APIs:

1. **packages** - Package registry data
2. **repos** - Repository data
3. **summary** - Summary data

Each API has its own set of operations that can be accessed through convenience commands or the generic `call` command.
