"""Base interface for evaluation pipelines."""

from abc import ABC, abstractmethod

from llm_evaluation_toolkit.core.project import Project


class Pipeline(ABC):
    """Defines an executable evaluation pipeline without supplying execution logic."""

    @abstractmethod
    def run(self, project: Project) -> None:
        """Execute the pipeline for a project."""
        raise NotImplementedError
