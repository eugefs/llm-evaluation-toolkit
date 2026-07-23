"""Metric registry."""

from llm_evaluation_toolkit.evaluation.protocols import Metric

from .exact_match import ExactMatchMetric
from .latency import LatencyMetric
from .token_usage import TokenUsageMetric


class MetricRegistry:
    """Registry for evaluation metrics."""

    _metrics: dict[str, type[Metric]] = {
        "exact_match": ExactMatchMetric,
        "latency": LatencyMetric,
        "token_usage": TokenUsageMetric,
    }

    @classmethod
    def get(
        cls,
        name: str,
    ) -> Metric:
        """Create metric instance."""

        try:
            metric_class = cls._metrics[name]
        except KeyError as exc:
            raise ValueError(
                f"Unknown metric: {name}",
            ) from exc

        return metric_class()