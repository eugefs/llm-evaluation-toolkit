"""Evaluation dataset models."""

from pydantic import BaseModel, ConfigDict, Field

from llm_evaluation_toolkit.evaluation.models import EvaluationCase


class EvaluationDataset(BaseModel):
    """A collection of evaluation cases."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str
    cases: list[EvaluationCase] = Field(default_factory=list)
    description: str | None = None

    @property
    def size(self) -> int:
        """Return the number of evaluation cases."""
        return len(self.cases)
