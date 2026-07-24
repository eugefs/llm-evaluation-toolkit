"""Experiment comparison reporting models."""

from pydantic import BaseModel, ConfigDict, Field


class ComparisonEntry(BaseModel):
    """Single provider comparison."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    first_score: float = Field(
        ge=0.0,
        le=1.0,
    )

    second_score: float = Field(
        ge=0.0,
        le=1.0,
    )

    score_delta: float


class PerformanceDelta(BaseModel):
    """Performance differences between runs."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    latency_delta: float = 0.0

    cost_delta: float = 0.0

    token_delta: int = 0


class ComparisonReport(BaseModel):
    """Full experiment comparison."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    entries: list[ComparisonEntry] = Field(
        default_factory=list,
    )

    performance: PerformanceDelta = Field(
        default_factory=PerformanceDelta,
    )