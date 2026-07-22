"""Metric registry."""

from llm_evaluation_toolkit.core.exceptions import MetricError
from llm_evaluation_toolkit.evaluation.protocols import Metric


class MetricRegistry:
    """Registry of available metrics."""

    def __init__(self) -> None:
        self._metrics: dict[str, Metric] = {}

    def register(self, metric: Metric) -> None:
        if metric.name in self._metrics:
            raise MetricError(
                f"Metric '{metric.name}' is already registered."
            )

        self._metrics[metric.name] = metric

    def unregister(self, name: str) -> None:
        if name not in self._metrics:
            raise MetricError(
                f"Metric '{name}' is not registered."
            )

        del self._metrics[name]

    def get(self, name: str) -> Metric:
        try:
            return self._metrics[name]
        except KeyError as exc:
            raise MetricError(
                f"Metric '{name}' is not registered."
            ) from exc

    def list_metrics(self) -> list[str]:
        return sorted(self._metrics.keys())
