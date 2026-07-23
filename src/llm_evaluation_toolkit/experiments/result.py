"""Experiment result models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from llm_evaluation_toolkit.evaluation import EvaluationReport


class ExperimentResult(BaseModel):
    """Persisted experiment execution result."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    reports: dict[str, EvaluationReport] = Field(
        default_factory=dict,
    )

    score: float = 0.0

    tokens_input: int = 0

    tokens_output: int = 0

    latency_ms: float = 0.0

    estimated_cost: float = 0.0