"""Base interface for persisted evaluation artifacts."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from uuid import UUID


class Artifact(ABC):
    """Describes immutable identity and descriptive data for an evaluation artifact."""

    @property
    @abstractmethod
    def id(self) -> UUID:
        """Return the artifact's unique identifier."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the human-readable artifact name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def metadata(self) -> dict[str, Any]:
        """Return descriptive metadata associated with the artifact."""
        raise NotImplementedError

    @property
    @abstractmethod
    def created_at(self) -> datetime:
        """Return the time at which the artifact was created."""
        raise NotImplementedError
