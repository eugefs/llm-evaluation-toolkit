"""Experiment comparison reporting."""

from pydantic import BaseModel, ConfigDict


class ComparisonEntry(BaseModel):
    """Single comparison value."""

    model_config = ConfigDict(
        frozen=True,
    )

    name: str

    first: float

    second: float

    delta: float


class ComparisonReport(BaseModel):
    """Comparison between experiment results."""

    model_config = ConfigDict(
        frozen=True,
    )

    entries: list[ComparisonEntry]

    latency_delta: float = 0.0

    cost_delta: float = 0.0

    token_delta: int = 0