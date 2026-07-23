"""Benchmark executor tests."""

from llm_evaluation_toolkit.benchmarks import (
    Benchmark,
    BenchmarkExecutor,
)
from llm_evaluation_toolkit.evaluation import (
    EvaluationDataset,
)
from llm_evaluation_toolkit.experiments import (
    ExperimentConfig,
)


class FakeRunner:
    """Fake experiment runner."""

    def run(
        self,
        config: ExperimentConfig,
        dataset: EvaluationDataset,
        provider_configs: dict[str, object],
    ) -> dict:
        """Return fake reports."""

        return {}


def test_benchmark_executor() -> None:
    """Execute benchmark through adapter."""

    benchmark = Benchmark(
        name="test-benchmark",
        version="1.0",
        dataset=EvaluationDataset(
            name="test-dataset",
            cases=[],
        ),
        cases=[],
    )

    config = ExperimentConfig(
        name="test-experiment",
        dataset="test-dataset",
        providers=[],
        metrics=[],
    )

    executor = BenchmarkExecutor(
        runner=FakeRunner(),
    )

    result = executor.run(
        benchmark=benchmark,
        config=config,
        provider_configs={},
    )

    assert result.name == "test-benchmark"
    assert result.reports == {}