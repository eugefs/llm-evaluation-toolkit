# llm-evaluation-toolkit

A lightweight toolkit for evaluating large language model outputs.

## Installation

Install the package and complete development toolchain from the repository
root:

```console
pip install -e ".[dev]"
```

## Development

Run the quality checks with:

```console
ruff check .
ruff format --check .
mypy
pytest
mkdocs build --strict
```

Install the Git hooks once with `pre-commit install`.
