.PHONY: help install install-dev test lint format docs docs-serve docs-deploy clean build

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install package dependencies"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  docs         - Build documentation"
	@echo "  docs-serve   - Serve documentation locally"
	@echo "  docs-deploy  - Deploy documentation to GitHub Pages"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"

# Install package
install:
	uv sync

# Install with development dependencies
install-dev:
	uv sync --extra dev

# Run tests
test:
	uv run pytest tests/

# Run linting
lint:
	uv run black --check hyperdb/ tests/
	uv run isort --check-only hyperdb/ tests/

# Format code
format:
	uv run black hyperdb/ tests/
	uv run isort hyperdb/ tests/

# Build documentation
docs:
	uv run --extra docs mkdocs build

# Serve documentation locally
docs-serve:
	uv run --extra docs mkdocs serve

# Deploy documentation to GitHub Pages
docs-deploy:
	uv run --extra docs mkdocs gh-deploy

# Clean build artifacts
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	uv build
