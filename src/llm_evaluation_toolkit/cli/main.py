"""CLI execution helpers."""

from pathlib import Path

from llm_evaluation_toolkit.benchmarks import (
    BenchmarkExecutor,
    BenchmarkLoader,
)
from llm_evaluation_toolkit.experiments import ExperimentStorage


def run_benchmark(
    benchmark_path: str,
    output: str,
    profile: str | None = None,
) -> None:
    """Run benchmark."""

    benchmark = BenchmarkLoader().load(
        Path(benchmark_path),
    )

    if profile is not None:
        benchmark = benchmark.select_profile(
            profile,
        )

    executor = BenchmarkExecutor()

    result = executor.run(
        benchmark=benchmark,
        provider_configs={},
    )

    storage = ExperimentStorage(
        Path(output),
    )

    saved_path = storage.save(
        result,
    )

    print(
        f"Benchmark completed: {result.name}",
    )

    print(
        f"Result saved: {saved_path}",
    )