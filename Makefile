.PHONY: bootstrap install test lint format typecheck check clean

bootstrap:
	pip install -e ".[dev]"
	pre-commit install

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

format:
	black .
	isort .

typecheck:
	mypy src

check:
	ruff check .
	black --check .
	isort --check-only .
	mypy src
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov build dist *.egg-info
