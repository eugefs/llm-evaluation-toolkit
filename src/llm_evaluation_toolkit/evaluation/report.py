"""Evaluation reporting models."""

from pydantic import BaseModel, ConfigDict, Field

from llm_evaluation_toolkit.evaluation.models import EvaluationResult


class EvaluationReport(BaseModel):
    """Aggregate statistics for an evaluation run."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    results: list[EvaluationResult] = Field(default_factory=list)

    @property
    def total_cases(self) -> int:
        """Return the total number of evaluated cases."""
        return len(self.results)

    @property
    def passed_cases(self) -> int:
        """Return the number of passing cases."""
        return sum(result.passed for result in self.results)

    @property
    def failed_cases(self) -> int:
        """Return the number of failing cases."""
        return self.total_cases - self.passed_cases

    @property
    def average_score(self) -> float:
        """Return the average evaluation score."""
        if not self.results:
            return 0.0

        return sum(result.score for result in self.results) / self.total_cases

    @property
    def pass_rate(self) -> float:
        """Return the fraction of passing cases."""
        if not self.results:
            return 0.0

        return self.passed_cases / self.total_cases