"""Configuration loader."""

import os
import re
from pathlib import Path
from typing import Any

import yaml

from .models import ProviderRunConfig


_ENV_PATTERN = re.compile(
    r"\$\{([^}]+)\}"
)


def _resolve_env(
    value: Any,
) -> Any:
    """Resolve environment variables recursively."""

    if isinstance(value, dict):
        return {
            key: _resolve_env(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _resolve_env(item)
            for item in value
        ]

    if isinstance(value, str):

        def replace(
            match: re.Match[str],
        ) -> str:
            variable = match.group(1)

            if variable not in os.environ:
                raise ValueError(
                    f"Missing environment variable: {variable}"
                )

            return os.environ[variable]

        return _ENV_PATTERN.sub(
            replace,
            value,
        )

    return value


def load_config(
    path: str | Path,
) -> ProviderRunConfig:
    """Load YAML configuration."""

    config_path = Path(path)

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data: dict[str, Any] = yaml.safe_load(file)

    resolved = _resolve_env(data)

    return ProviderRunConfig.model_validate(
        resolved
    )