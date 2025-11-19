"""Domain logic for the DubaiAthan application."""

from __future__ import annotations

from datetime import date
from typing import Dict, Optional

from core.config import load_config
from core.prayer_api import PrayerAPI
from core.scheduler import AthanScheduler


class AthanManager:
    """Coordinates fetching data, applying settings, and scheduling."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        self.config = load_config(config_path)
        location = self.config.get("location", {})
        api_cfg = self.config.get("api", {})

        self.api = PrayerAPI(
            base_url=api_cfg.get("base_url"),
            city_id=location.get("city_id", 1),
            timeout=int(api_cfg.get("timeout", 10)),
        )
        self.scheduler = AthanScheduler(timezone=location.get("timezone", "Asia/Dubai"))
        self.settings: Dict[str, object] = {"theme": self.config.get("ui", {}).get("theme", "desert")}
        self._cached_schedule: Dict[str, str] = {}
        self._cached_date: date | None = None

    def refresh_schedule(self, target_date: Optional[date] = None) -> Dict[str, str]:
        """Fetch the latest schedule from the remote API."""
        schedule = self.api.fetch_daily_schedule(target_date)
        self._cached_date = target_date or date.today()
        self._cached_schedule = schedule
        self.scheduler.schedule_day(schedule, self._cached_date)
        return schedule

    def get_prayer_schedule(self, target_date: Optional[date] = None) -> Dict[str, str]:
        """Return the cached schedule, refreshing if necessary."""
        if (
            not self._cached_schedule
            or target_date is not None
            and target_date != self._cached_date
        ):
            return self.refresh_schedule(target_date)
        return self._cached_schedule

    def get_timezone(self) -> str:
        """Return the currently configured timezone."""
        return str(self.scheduler.configuration.get("timezone", "Asia/Dubai"))

    def get_cached_date(self) -> date:
        """Expose the date for which the schedule is cached."""
        return self._cached_date or date.today()

    def apply_settings(self, settings: Dict[str, object]) -> None:
        """Store settings and update scheduler if relevant."""
        self.settings.update(settings)
        self.scheduler.configure(settings)
