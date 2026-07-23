"""Plugin registry tests."""

from llm_evaluation_toolkit.plugins import PluginRegistry


class ExamplePlugin:
    """Example plugin."""
    

def test_plugin_registry_registers_plugin() -> None:
    """Registry returns plugin."""

    PluginRegistry.register(
        "example",
        ExamplePlugin,
    )

    plugin = PluginRegistry.get(
        "example",
    )

    assert plugin is ExamplePlugin