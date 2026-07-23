"""Benchmark environment tests."""

from pathlib import Path

from llm_evaluation_toolkit.benchmarks import (
    BenchmarkLoader,
)


def test_benchmark_resolves_environment(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Benchmark loader resolves variables."""

    monkeypatch.setenv(
        "TEST_MODEL",
        "gpt-5",
    )

    file = tmp_path / "benchmark.yaml"

    file.write_text(
        """
name: env-test
version: "1.0"

providers:
  - name: openai
    model: ${TEST_MODEL}

dataset:
  name: test
  cases: []
""",
        encoding="utf-8",
    )

    benchmark = BenchmarkLoader().load(
        file,
    )

    assert benchmark.providers[0].model == "gpt-5"