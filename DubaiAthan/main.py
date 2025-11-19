"""Entry point for the DubaiAthan application."""

from core.athan_manager import AthanManager
from ui.dashboard import Dashboard
from ui.settings import Settings


def main() -> None:
    """Bootstrap the app and simulate simple interactions."""
    manager = AthanManager()
    dashboard = Dashboard(manager)
    settings = Settings(manager)

    settings.load_user_preferences()
    dashboard.render()


if __name__ == "__main__":
    main()
