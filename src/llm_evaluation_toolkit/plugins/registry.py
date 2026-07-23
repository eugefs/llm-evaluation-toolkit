"""Plugin registry."""

from typing import TypeVar


T = TypeVar(
    "T",
)


class PluginRegistry:
    """Registry for external plugins."""

    _plugins: dict[str, type[object]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        plugin: type[T],
    ) -> None:
        """Register plugin."""

        cls._plugins[name] = plugin

    @classmethod
    def get(
        cls,
        name: str,
    ) -> type[object]:
        """Get plugin."""

        if name not in cls._plugins:
            raise ValueError(
                f"Unknown plugin: {name}",
            )

        return cls._plugins[name]

    @classmethod
    def available(
        cls,
    ) -> list[str]:
        """Return plugins."""

        return list(
            cls._plugins.keys(),
        )