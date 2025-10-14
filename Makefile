.PHONY: help sync install test coverage lint format clean

help:
	@echo "Available commands:"
	@echo "  make sync      - Sync dependencies and setup environment"
	@echo "  make install   - Install all dependencies"
	@echo "  make test      - Run all tests"
	@echo "  make coverage  - Run tests with coverage report"
	@echo "  make lint      - Run linting checks"
	@echo "  make format    - Format code with black and isort"
	@echo "  make clean     - Clean up generated files"

sync: install
	@echo "✓ Dependencies synced"

install:
	@echo "Installing dependencies..."
	@if command -v uv > /dev/null 2>&1; then \
		uv pip install -e ".[dev]"; \
	else \
		python3 -m pip install -e ".[dev]"; \
	fi
	@echo "✓ Dependencies installed"

test:
	@echo "Running tests..."
	@pytest -v

coverage:
	@echo "Running tests with coverage..."
	@pytest --cov=. --cov-report=term-missing --cov-report=html --cov-fail-under=80

lint:
	@echo "Running linting checks..."
	@ruff check .
	@black --check .
	@mypy .

format:
	@echo "Formatting code..."
	@ruff check . --fix
	@black .
	@isort .

clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "✓ Cleaned up"
