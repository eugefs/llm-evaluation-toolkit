"""Tests for core project abstractions."""

from llm_evaluation_toolkit.core import Project


def test_project_can_be_constructed() -> None:
    """A project is represented by its name."""
    project = Project(name="baseline")

    assert project.name == "baseline"
