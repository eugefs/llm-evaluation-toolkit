# Contributing

## Development setup

Use Python 3.13 or later, then install the project from the repository root:

```console
pip install -e ".[dev]"
pre-commit install
```

## Quality checks

Run the complete local validation suite before opening a pull request:

```console
ruff check .
ruff format --check .
mypy
pytest --cov
mkdocs build --strict
```
