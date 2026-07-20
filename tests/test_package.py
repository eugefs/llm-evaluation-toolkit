"""Smoke tests for the package skeleton."""

from llm_evaluation_toolkit import __version__


def test_version_is_defined() -> None:
    assert __version__ == "0.1.0"
