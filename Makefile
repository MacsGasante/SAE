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
	ruff format .
	ruff check --fix .

typecheck:
	mypy src

check:
	ruff check .
	ruff format --check .
	mypy src
	pytest --cov=src/sae --cov-report=term-missing
	coverage report --include="src/sae/kernel/*" --fail-under=100

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov build dist *.egg-info
