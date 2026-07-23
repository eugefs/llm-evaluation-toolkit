"""Benchmark execution adapter."""

from llm_evaluation_toolkit.experiments import (
    ExperimentConfig,
    ExperimentResult,
    ExperimentRunner,
)

from .models import Benchmark


class BenchmarkExecutor:
    """Execute benchmarks through experiments."""

    def __init__(
        self,
        runner: ExperimentRunner | None = None,
    ) -> None:
        """Initialize executor."""

        self._runner = runner or ExperimentRunner()

    def run(
        self,
        benchmark: Benchmark,
        provider_configs: dict[str, object] | None = None,
        config: ExperimentConfig | None = None,
    ) -> ExperimentResult:
        """Execute benchmark."""

        if config is None:
            config = self._create_experiment_config(
                benchmark,
            )

        reports = self._runner.run(
            config=config,
            dataset=benchmark.dataset,
            provider_configs=provider_configs or {},
        )

        return ExperimentResult(
            name=benchmark.name,
            reports=reports,
        )

    def _create_experiment_config(
        self,
        benchmark: Benchmark,
    ) -> ExperimentConfig:
        """Create experiment config from benchmark."""

        return ExperimentConfig(
            name=benchmark.name,
            description=benchmark.description,
            providers=[
                provider.name
                for provider in benchmark.providers
            ],
            metrics=[
                metric.name
                for metric in benchmark.metrics
            ],
            dataset=benchmark.dataset.name,
        )