"""Experiment comparison models."""

from pydantic import BaseModel, ConfigDict, Field

from .result import ExperimentResult


class ProviderRanking(BaseModel):
    """Provider ranking entry."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    provider: str = Field(
        min_length=1,
    )

    average_score: float = Field(
        ge=0.0,
        le=1.0,
    )


class ExperimentComparison(BaseModel):
    """Comparison between experiment results."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    ranking: list[ProviderRanking] = Field(
        default_factory=list,
    )

    @classmethod
    def from_results(
        cls,
        results: dict[str, ExperimentResult],
    ) -> "ExperimentComparison":
        """Build comparison from experiment results."""

        ranking: list[ProviderRanking] = []

        for provider, result in results.items():
            scores = [
                report.average_score
                for report in result.reports.values()
            ]

            average = (
                sum(scores) / len(scores)
                if scores
                else 0.0
            )

            ranking.append(
                ProviderRanking(
                    provider=provider,
                    average_score=average,
                )
            )

        ranking.sort(
            key=lambda item: item.average_score,
            reverse=True,
        )

        return cls(
            ranking=ranking,
        )