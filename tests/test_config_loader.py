"""Configuration loader tests."""

from pathlib import Path

import pytest

from llm_evaluation_toolkit.config import load_config


def test_load_yaml_config(
    tmp_path: Path,
) -> None:
    """Load configuration from YAML."""

    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
provider: openai
api_key: test-key

model:
  name: test-model
  temperature: 0.0
  max_tokens: 100
""",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config.provider == "openai"
    assert config.api_key == "test-key"
    assert config.model.name == "test-model"


def test_load_config_with_environment_variable(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Resolve environment variables."""

    monkeypatch.setenv(
        "TEST_API_KEY",
        "secret-key",
    )

    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
provider: anthropic
api_key: ${TEST_API_KEY}

model:
  name: claude-test
""",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config.api_key == "secret-key"


def test_missing_environment_variable(
    tmp_path: Path,
) -> None:
    """Fail when environment variable is missing."""

    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
provider: xai
api_key: ${MISSING_KEY}

model:
  name: grok-test
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_config(config_file)