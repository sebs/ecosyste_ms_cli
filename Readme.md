# Ecosystems CLI

[![Build-Test-Lint](https://github.com/sebs/ecosyste_ms_cli/actions/workflows/build-test-lint.yml/badge.svg)](https://github.com/sebs/ecosyste_ms_cli/actions/workflows/build-test-lint.yml)
[![Latest Release](https://img.shields.io/github/v/release/sebs/ecosyste_ms_cli)](https://github.com/sebs/ecosyste_ms_cli/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line interface for interacting with ecosyste.ms APIs.

## Installation

Requirements:
- Python 3.12+

```bash
# Clone the repository
git clone git@github.com:sebs/ecosyste_ms_cli.git
cd ecosyste_ms_cli

# Set up virtual environment and install dependencies
make setup
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


## Output Formats

The CLI supports multiple output formats:

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

## Available Commands

### Repos API
- `repos topics` - List all topics
- `repos topic` - Get a specific topic
- `repos hosts` - List all repository hosts
- `repos host` - Get a specific host
- `repos repository` - Get a specific repository
- `repos list` - List available operations
- `repos call` - Call an operation directly

### Packages API
- `packages registries` - List all registries
- `packages registry` - Get a specific registry
- `packages package` - Get a specific package
- `packages version` - Get a specific package version
- `packages list` - List available operations
- `packages call` - Call an operation directly

### Summary API
- `summary repo` - Get repository summary
- `summary package` - Get package summary
- `summary list` - List available operations
- `summary call` - Call an operation directly

### Awesome API
- `awesome projects` - List all projects
- `awesome project` - Get a specific project
- `awesome lists` - List all lists
- `awesome list` - Get a specific list
- `awesome list-projects` - Get projects in a list
- `awesome topics` - List all topics
- `awesome topic` - Get a specific topic
- `awesome operations` - List available operations
- `awesome call` - Call an operation directly

### Papers API
- `papers list-papers` - List all papers
- `papers get` - Get a specific paper by DOI
- `papers mentions` - List all mentions for a paper
- `papers list` - List available operations
- `papers call` - Call an operation directly

## Examples

```bash
# Get all projects from the awesome API
ecosystems awesome projects

# List papers with pagination
ecosystems papers list-papers --page 1 --per-page 10

# Get a specific paper by DOI
ecosystems papers get "10.1234/example"

# Get mentions for a paper
ecosystems papers mentions "10.1234/example"
```

## Documentation

- [Development Guide](Development.md) - Information about development, testing, and release processes
- [Changelog](CHANGELOG.md) - History of changes and releases
- [License](LICENSE) - MIT License details
