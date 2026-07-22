"""Run storage tests."""

from datetime import datetime
from pathlib import Path

from llm_evaluation_toolkit.runs.models import (
    RunMetadata,
    RunRequest,
    RunResponse,
)
from llm_evaluation_toolkit.runs.storage import (
    RunStorage,
)


def test_save_run(
    tmp_path: Path,
) -> None:
    """Persist a complete run."""

    storage = RunStorage(
        root=tmp_path,
    )

    metadata = RunMetadata(
        run_id="test-run-001",
        created_at=datetime.now(),
        provider="openai",
        model="test-model",
        temperature=0.0,
        max_tokens=100,
    )

    request = RunRequest(
        prompt="Hello",
    )

    response = RunResponse(
        content="Hello world",
        finish_reason="stop",
        total_tokens=10,
    )

    run_path = storage.save(
        metadata,
        request,
        response,
    )

    assert run_path.exists()

    assert (
        run_path / "metadata.json"
    ).exists()

    assert (
        run_path / "request.json"
    ).exists()

    assert (
        run_path / "response.json"
    ).exists()


def test_storage_creates_directory(
    tmp_path: Path,
) -> None:
    """Storage creates root directory."""

    root = tmp_path / "custom-runs"

    RunStorage(root=root)

    assert root.exists()