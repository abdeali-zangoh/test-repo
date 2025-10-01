.PHONY: sync test coverage clean

sync:
	uv pip install pytest pytest-cov

test:
	uv run pytest

coverage:
	uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90

clean:
	rm -rf .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
