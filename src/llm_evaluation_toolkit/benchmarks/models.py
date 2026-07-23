"""Benchmark models."""

from pydantic import BaseModel, ConfigDict, Field

from llm_evaluation_toolkit.evaluation import EvaluationDataset

from .metadata import BenchmarkMetadata
from .profiles import BenchmarkProfile


class BenchmarkCase(BaseModel):
    """Single benchmark metadata."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: str = Field(
        min_length=1,
    )

    category: str | None = None

    tags: list[str] = Field(
        default_factory=list,
    )


class BenchmarkProvider(BaseModel):
    """Provider configuration."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    model: str | None = None


class BenchmarkMetric(BaseModel):
    """Metric configuration."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )


class Benchmark(BaseModel):
    """Benchmark definition."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    version: str = Field(
        min_length=1,
    )

    description: str | None = None

    metadata: BenchmarkMetadata | None = None

    dataset: EvaluationDataset

    providers: list[BenchmarkProvider] = Field(
        default_factory=list,
    )

    metrics: list[BenchmarkMetric] = Field(
        default_factory=list,
    )

    profiles: list[BenchmarkProfile] = Field(
        default_factory=list,
    )

    cases: list[BenchmarkCase] = Field(
        default_factory=list,
    )

    def select_profile(
        self,
        name: str,
    ) -> "Benchmark":
        """Return benchmark using selected profile."""

        for profile in self.profiles:
            if profile.name == name:
                return self.model_copy(
                    update={
                        "providers": [
                            BenchmarkProvider(
                                name=provider.name,
                                model=provider.model,
                            )
                            for provider in profile.providers
                        ],
                    },
                )

        raise ValueError(
            f"Unknown profile: {name}",
        )