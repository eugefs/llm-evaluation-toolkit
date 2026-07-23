"""Run tracker tests."""

import json
from pathlib import Path

from llm_evaluation_toolkit.runs import (
    RunStorage,
    RunTracker,
)


def test_tracker_records_run(
    tmp_path: Path,
) -> None:
    """Tracker should create persisted run."""

    storage = RunStorage(
        root=tmp_path,
    )

    tracker = RunTracker(
        storage=storage,
    )

    run_path = tracker.record(
        provider="openai",
        model="test-model",
        temperature=0.0,
        max_tokens=100,
        prompt="Hello",
        content="Hello world",
        finish_reason="stop",
        total_tokens=10,
    )

    assert run_path.exists()

    metadata_file = (
        run_path / "metadata.json"
    )

    response_file = (
        run_path / "response.json"
    )

    assert metadata_file.exists()
    assert response_file.exists()

    metadata = json.loads(
        metadata_file.read_text(
            encoding="utf-8",
        )
    )

    response = json.loads(
        response_file.read_text(
            encoding="utf-8",
        )
    )

    assert metadata["provider"] == "openai"
    assert metadata["model"] == "test-model"
    assert response["content"] == "Hello world"


def test_tracker_generates_unique_runs(
    tmp_path: Path,
) -> None:
    """Each tracked run gets a unique id."""

    tracker = RunTracker(
        storage=RunStorage(
            root=tmp_path,
        )
    )

    first = tracker.record(
        provider="xai",
        model="grok-test",
        temperature=0.0,
        max_tokens=50,
        prompt="A",
        content="B",
    )

    second = tracker.record(
        provider="xai",
        model="grok-test",
        temperature=0.0,
        max_tokens=50,
        prompt="C",
        content="D",
    )

    assert first != second