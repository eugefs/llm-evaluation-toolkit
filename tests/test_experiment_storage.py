"""Experiment storage tests."""

from pathlib import Path

from llm_evaluation_toolkit.evaluation import (
    EvaluationReport,
)
from llm_evaluation_toolkit.experiments import (
    ExperimentResult,
    ExperimentStorage,
)


def test_experiment_storage_save_and_load(
    tmp_path: Path,
) -> None:
    """Save and load experiment result."""

    storage = ExperimentStorage(
        directory=tmp_path,
    )

    result = ExperimentResult(
        name="test-experiment",
        reports={
            "openai": EvaluationReport(
                results=[],
            ),
        },
    )

    saved_path = storage.save(
        result,
    )

    assert saved_path.exists()

    loaded = storage.load(
        "test-experiment",
    )

    assert loaded.name == result.name
    assert "openai" in loaded.reports