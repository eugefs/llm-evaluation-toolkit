"""Generation capability protocol."""

from typing import Protocol

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
)


class Generator(Protocol):
    """Protocol implemented by providers capable of text generation."""

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response."""
        ...