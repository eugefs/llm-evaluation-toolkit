"""Tests for the command-line application definition."""

from typer.testing import CliRunner

from llm_evaluation_toolkit.cli import app


def test_cli_application_is_defined() -> None:
    """The package exposes a Typer application for the console entry point."""
    assert app is not None


def test_cli_help_displays_project_name() -> None:
    """The console application identifies the toolkit in its help output."""
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "LLM Evaluation Toolkit" in result.output
