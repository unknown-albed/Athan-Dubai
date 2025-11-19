"""Settings UI placeholder."""

from __future__ import annotations

from core.athan_manager import AthanManager


class Settings:
    """Fake settings panel that interacts with the athan manager."""

    def __init__(self, manager: AthanManager) -> None:
        self.manager = manager

    def load_user_preferences(self) -> None:
        """Pretend to load preferences and apply them to the manager."""
        prefs = {
            "theme": self.manager.settings.get("theme", "desert"),
            "notifications": True,
        }
        self.manager.apply_settings(prefs)
