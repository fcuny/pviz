# List all available commands
default:
    @just --list

# Run tests
test:
    uv run pytest

# Run tests with coverage report
coverage:
    uv run pytest --cov=pviz --cov-report=term-missing

# Run linter
lint:
    uvx ruff check .

# Auto-fix linting issues where possible
lint-fix:
    uvx ruff check --fix .

# Format code
format:
    uvx ruff format .

# Run all checks (lint and test)
check: lint test

# Build the package
build:
    uv pip install build
    uv run python -m build

# Run the CLI tool with arguments
run *ARGS:
    uv run pviz {{ARGS}}
