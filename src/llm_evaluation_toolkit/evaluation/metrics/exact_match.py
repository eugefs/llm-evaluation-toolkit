"""Exact match evaluation metric."""

from llm_evaluation_toolkit.evaluation.models import EvaluationCase
from llm_evaluation_toolkit.evaluation.protocols import Metric
from llm_evaluation_toolkit.generation import GenerationResponse


class ExactMatchMetric(Metric):
    """Scores 1.0 when the response exactly matches the expected output."""

    @property
    def name(self) -> str:
        """Return the metric name."""
        return "exact_match"

    def score(
        self,
        case: EvaluationCase,
        response: GenerationResponse,
    ) -> float:
        """Return a normalized exact-match score."""

        return (
            1.0
            if response.content == case.expected_output
            else 0.0
        )