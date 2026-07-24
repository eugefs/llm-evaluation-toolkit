"""Experiment runner."""

from llm_evaluation_toolkit.evaluation import (
    EvaluationDataset,
    EvaluationReport,
    Evaluator,
)
from llm_evaluation_toolkit.evaluation.protocols import Metric
from llm_evaluation_toolkit.providers import (
    Generator,
    ProviderRegistry,
)

from .models import ExperimentConfig


class ExperimentRunner:
    """Run configured experiments."""

    def __init__(
        self,
        registry: type[ProviderRegistry] = ProviderRegistry,
    ) -> None:
        """Initialize runner."""

        self._registry = registry

    def run(
        self,
        config: ExperimentConfig,
        dataset: EvaluationDataset,
        provider_configs: dict[str, object],
    ) -> dict[str, EvaluationReport]:
        """Run experiment across providers."""

        reports: dict[str, EvaluationReport] = {}

        for provider_name in config.providers:
            provider = self._registry.create(
                provider_name,
                provider_configs[provider_name],
            )

            if not isinstance(provider, Generator):
                raise TypeError(
                    f"Provider '{provider_name}' "
                    "does not support generation",
                )

            generator = provider

            metrics = [
                self._resolve_metric(metric_name)
                for metric_name in config.metrics
            ]

            evaluator = Evaluator(
                generator=generator,
                metrics=metrics,
            )

            results = evaluator.evaluate_dataset(
                dataset,
            )

            reports[provider_name] = EvaluationReport(
                results=results,
            )

        return reports

    def _resolve_metric(
        self,
        name: str,
    ) -> Metric:
        """Resolve metric by name."""

        from llm_evaluation_toolkit.evaluation.metrics import (
            ExactMatchMetric,
            LatencyMetric,
            TokenUsageMetric,
        )

        metrics: dict[str, type[Metric]] = {
            "exact_match": ExactMatchMetric,
            "latency": LatencyMetric,
            "token_usage": TokenUsageMetric,
        }

        metric_class = metrics.get(name)

        if metric_class is None:
            raise ValueError(
                f"Unknown metric: {name}",
            )

        return metric_class()