"""Provider creation from configuration tests."""

from pathlib import Path

from llm_evaluation_toolkit.config import (
    create_provider_from_config,
)
from llm_evaluation_toolkit.providers import (
    Provider,
)


def test_create_provider_from_yaml(
    tmp_path: Path,
) -> None:
    """Create provider using YAML configuration."""

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

    provider = create_provider_from_config(
        str(config_file),
    )

    assert isinstance(
        provider,
        Provider,
    )

    assert provider.name == "openai"


def test_create_anthropic_provider_from_yaml(
    tmp_path: Path,
) -> None:
    """Create Anthropic provider from YAML."""

    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
provider: anthropic
api_key: test-key

model:
  name: claude-test
""",
        encoding="utf-8",
    )

    provider = create_provider_from_config(
        str(config_file),
    )

    assert provider.name == "anthropic"