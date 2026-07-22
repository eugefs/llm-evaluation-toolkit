"""Experiment models."""

from pydantic import BaseModel, ConfigDict, Field


class ExperimentConfig(BaseModel):
    """Configuration for an experiment run."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    description: str | None = None

    providers: list[str] = Field(
        default_factory=list,
    )

    metrics: list[str] = Field(
        default_factory=list,
    )

    dataset: str