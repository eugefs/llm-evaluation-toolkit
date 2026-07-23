"""Plugin loader tests."""

from llm_evaluation_toolkit.plugins import PluginLoader


def test_plugin_loader_has_group() -> None:
    """Loader defines entry point group."""

    assert (
        PluginLoader.GROUP
        == "llm_evaluation_toolkit.plugins"
    )