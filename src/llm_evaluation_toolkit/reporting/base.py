"""Structural interface for evaluation reporters."""

from typing import Protocol, runtime_checkable

from llm_evaluation_toolkit.core.project import Project


@runtime_checkable
class Reporter(Protocol):
    """Defines an object that can report results for an evaluation project."""

    def report(self, project: Project) -> None:
        """Report the results associated with a project."""
        ...
