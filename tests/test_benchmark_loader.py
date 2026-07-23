"""Benchmark loader tests."""

from pathlib import Path

from llm_evaluation_toolkit.benchmarks import (
    BenchmarkLoader,
)


def test_load_yaml_benchmark(
    tmp_path: Path,
) -> None:
    """Load benchmark from YAML."""

    benchmark_file = tmp_path / "benchmark.yaml"

    benchmark_file.write_text(
        """
name: qa-benchmark
version: "1.0"

description: Test benchmark

dataset:
  name: qa-dataset
  cases:
    - id: "case-1"
      request:
        messages:
          - role: user
            content: "What is AI?"
      expected_output: "Artificial Intelligence"

cases:
  - id: "case-1"
    category: knowledge
    tags:
      - factual
""",
        encoding="utf-8",
    )

    benchmark = BenchmarkLoader().load(
        benchmark_file,
    )

    assert benchmark.name == "qa-benchmark"
    assert benchmark.version == "1.0"
    assert benchmark.dataset.name == "qa-dataset"
    assert len(benchmark.cases) == 1
    assert benchmark.cases[0].category == "knowledge"


def test_load_json_benchmark(
    tmp_path: Path,
) -> None:
    """Load benchmark from JSON."""

    benchmark_file = tmp_path / "benchmark.json"

    benchmark_file.write_text(
        """
{
  "name": "json-benchmark",
  "version": "1.0",
  "dataset": {
    "name": "json-dataset",
    "cases": []
  },
  "cases": []
}
""",
        encoding="utf-8",
    )

    benchmark = BenchmarkLoader().load(
        benchmark_file,
    )

    assert benchmark.name == "json-benchmark"
    assert benchmark.dataset.name == "json-dataset"