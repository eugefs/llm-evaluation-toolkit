"""Project definition for evaluation workspaces."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Project:
    """Identifies an evaluation project without prescribing its implementation."""

    name: str
