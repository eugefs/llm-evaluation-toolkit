"""Tests for artifact, provider, pipeline, and reporter contracts."""

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID, uuid4

import pytest

from llm_evaluation_toolkit.artifacts import Artifact
from llm_evaluation_toolkit.core import Project
from llm_evaluation_toolkit.pipelines import Pipeline
from llm_evaluation_toolkit.providers import Provider
from llm_evaluation_toolkit.reporting import Reporter


class ExampleArtifact(Artifact):
    """Concrete artifact used to verify the abstract contract."""

    def __init__(self) -> None:
        """Create a complete artifact fixture."""
        self._id = uuid4()
        self._created_at = datetime.now(UTC)

    @property
    def id(self) -> UUID:
        """Return the fixture identifier."""
        return self._id

    @property
    def name(self) -> str:
        """Return the fixture name."""
        return "example"

    @property
    def metadata(self) -> dict[str, Any]:
        """Return the fixture metadata."""
        return {"kind": "test"}

    @property
    def created_at(self) -> datetime:
        """Return the fixture timestamp."""
        return self._created_at


class ExamplePipeline(Pipeline):
    """Concrete pipeline used to verify the abstract contract."""

    def run(self, project: Project) -> None:
        """Provide the required interface without application behavior."""
        del project


class ExampleProvider:
    """Structural provider implementation used for runtime protocol checks."""

    name = "example"


class ExampleReporter:
    """Structural reporter implementation used for runtime protocol checks."""

    def report(self, project: Project) -> None:
        """Provide the required reporting signature."""
        del project


def test_artifact_abstract_class_cannot_be_constructed() -> None:
    """Artifacts require all descriptive properties to be supplied."""
    with pytest.raises(TypeError):
        Artifact()  # type: ignore[abstract]


def test_artifact_contract_can_be_constructed() -> None:
    """A complete Artifact implementation exposes every required value."""
    artifact = ExampleArtifact()

    assert isinstance(artifact.id, UUID)
    assert artifact.name == "example"
    assert artifact.metadata == {"kind": "test"}
    assert artifact.created_at.tzinfo is UTC


@pytest.mark.parametrize(
    "getter",
    [
        cast(Any, Artifact.id).fget,
        cast(Any, Artifact.name).fget,
        cast(Any, Artifact.metadata).fget,
        cast(Any, Artifact.created_at).fget,
    ],
)
def test_artifact_abstract_getters_raise_not_implemented(
    getter: Callable[[Artifact], object] | None,
) -> None:
    """Abstract property implementations explicitly reject direct use."""
    assert getter is not None
    with pytest.raises(NotImplementedError):
        getter(cast(Artifact, object()))


def test_pipeline_abstract_class_cannot_be_constructed() -> None:
    """Pipelines require a run implementation."""
    with pytest.raises(TypeError):
        Pipeline()  # type: ignore[abstract]


def test_pipeline_contract_can_be_constructed() -> None:
    """A complete Pipeline implementation can be instantiated and invoked."""
    pipeline = ExamplePipeline()

    pipeline.run(Project(name="baseline"))


def test_pipeline_base_method_raises_not_implemented() -> None:
    """The base pipeline has no execution behavior."""
    with pytest.raises(NotImplementedError):
        Pipeline.run(ExamplePipeline(), Project(name="baseline"))


def test_provider_protocol_is_runtime_checkable() -> None:
    """Providers can be checked structurally at runtime."""
    provider = ExampleProvider()

    assert isinstance(provider, Provider)
    assert provider.name == "example"

    name_getter = cast(Any, Provider.name).fget
    assert name_getter is not None

    # Protocol placeholder implementations return None when invoked.
    assert name_getter(cast(Provider, provider)) is None


def test_provider_protocol_cannot_be_constructed() -> None:
    """Protocols define contracts rather than concrete instances."""
    with pytest.raises(TypeError):
        Provider()  # type: ignore[misc]


def test_reporter_protocol_is_runtime_checkable() -> None:
    """Reporters can be checked structurally at runtime."""
    reporter = ExampleReporter()

    assert isinstance(reporter, Reporter)

    reporter.report(Project(name="baseline"))
    Reporter.report(reporter, Project(name="baseline"))


def test_reporter_protocol_cannot_be_constructed() -> None:
    """Protocols define contracts rather than concrete instances."""
    with pytest.raises(TypeError):
        Reporter()  # type: ignore[misc]