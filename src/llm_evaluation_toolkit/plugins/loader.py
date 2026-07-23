"""Plugin discovery loader."""

from importlib.metadata import entry_points

from .registry import PluginRegistry


class PluginLoader:
    """Load installed plugins."""

    GROUP = (
        "llm_evaluation_toolkit.plugins"
    )

    @classmethod
    def discover(cls) -> None:
        """Discover installed plugins."""

        plugins = entry_points()

        for plugin in plugins.select(
            group=cls.GROUP,
        ):
            loaded = plugin.load()

            PluginRegistry.register(
                plugin.name,
                loaded,
            )