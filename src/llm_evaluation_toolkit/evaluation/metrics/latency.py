"""Latency metric."""

from typing import Any

from llm_evaluation_toolkit.evaluation.models import (
    EvaluationCase,
)
from llm_evaluation_toolkit.generation import (
    GenerationResponse,
)


class LatencyMetric:
    """Measure generation latency."""

    @property
    def name(self) -> str:
        """Return metric name."""
        return "latency"

    def score(
        self,
        case: EvaluationCase,
        response: GenerationResponse,
    ) -> float:
        """Return normalized latency score."""

        metadata: dict[str, Any] = getattr(
            case,
            "metadata",
            {},
        )

        latency_value = metadata.get(
            "latency",
        )

        if latency_value is None:
            return 0.0

        latency = float(latency_value)

        if latency <= 1.0:
            return 1.0

        if latency >= 10.0:
            return 0.0

        return max(
            0.0,
            1.0 - ((latency - 1.0) / 9.0),
        )