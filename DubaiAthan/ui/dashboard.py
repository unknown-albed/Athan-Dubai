"""Dashboard UI placeholder."""

from __future__ import annotations

from core.athan_manager import AthanManager


class Dashboard:
    """Simple dashboard mock that renders prayer times."""

    def __init__(self, manager: AthanManager) -> None:
        self.manager = manager

    def render(self) -> None:
        """Display the current day's prayer schedule in the console."""
        schedule = self.manager.get_prayer_schedule()
        tz = self.manager.get_timezone()
        day = self.manager.get_cached_date()
        print(f"DubaiAthan Dashboard — {day.isoformat()} ({tz})")
        for name, time_str in schedule.items():
            print(f" - {name.title()}: {time_str}")
