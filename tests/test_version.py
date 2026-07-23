"""Package version tests."""

from llm_evaluation_toolkit import __version__


def test_version_exists() -> None:
    """Package exposes version."""

    assert __version__
    assert __version__ == "0.1.0"