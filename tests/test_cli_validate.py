"""CLI validation tests."""

from pathlib import Path

from typer.testing import CliRunner

from llm_evaluation_toolkit.cli import app


runner = CliRunner()


def test_validate_valid_benchmark(
    tmp_path: Path,
) -> None:
    """Validate a correct benchmark."""

    file = tmp_path / "benchmark.yaml"

    file.write_text(
        """
name: test
version: "1.0"

dataset:
  name: dataset
  cases: []
""",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "validate",
            str(file),
        ],
    )

    assert result.exit_code == 0
    assert "Benchmark is valid" in result.output