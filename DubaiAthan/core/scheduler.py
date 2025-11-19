"""Simple scheduler placeholder."""

from __future__ import annotations

from datetime import date
from typing import Dict, Optional


class AthanScheduler:
    """Mock scheduler for playing athan audio."""

    def __init__(self, timezone: str = "Asia/Dubai") -> None:
        self.configuration: Dict[str, object] = {"timezone": timezone}
        self.tasks: Dict[str, str] = {}

    def configure(self, settings: Dict[str, object]) -> None:
        """Store configuration options such as theme or notifications."""
        self.configuration.update(settings)

    def schedule_day(self, schedule: Dict[str, str], day: Optional[date] = None) -> None:
        """Store the schedule as if we had scheduled notification tasks."""
        day_label = day.isoformat() if day else "unspecified"
        self.tasks = {f"{day_label}:{name}": time_str for name, time_str in schedule.items()}
