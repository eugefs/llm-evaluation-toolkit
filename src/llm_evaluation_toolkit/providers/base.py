"""Structural interface for evaluation providers."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Provider(Protocol):
    """Defines the identifying information exposed by an evaluation provider."""

    @property
    def name(self) -> str:
        """Return the provider's human-readable name."""
        ...
