"""Evaluation protocols."""

from typing import Protocol

from llm_evaluation_toolkit.evaluation.models import EvaluationCase
from llm_evaluation_toolkit.generation import GenerationResponse


class Metric(Protocol):
    """Protocol implemented by evaluation metrics."""

    @property
    def name(self) -> str:
        """Return the metric name."""
        ...

    def score(
        self,
        case: EvaluationCase,
        response: GenerationResponse,
    ) -> float:
        """Return a normalized score in the range [0.0, 1.0]."""
        ...