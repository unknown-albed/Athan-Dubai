"""Prayer time API client."""

from __future__ import annotations

import json
from datetime import date
from typing import Dict, Iterable
from urllib import error, request


class PrayerAPI:
    """Tiny API wrapper with fallback data."""

    def __init__(self, base_url: str, city_id: int = 1, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("?")
        self.city_id = city_id
        self.timeout = timeout

    def build_url(self, month: int, year: int) -> str:
        """Compose the request URL for a particular month/year."""
        return f"{self.base_url}?month={month}&year={year}&cityid={self.city_id}"

    def fetch_daily_schedule(self, target_date: date | None = None) -> Dict[str, str]:
        """Fetch prayer schedule and return structured data."""
        target_date = target_date or date.today()
        url = self.build_url(target_date.month, target_date.year)
        try:
            with request.urlopen(url, timeout=self.timeout) as response:
                payload = response.read()
            data = json.loads(payload.decode("utf-8"))
            parsed = self._extract_schedule(data, target_date)
            if parsed:
                return parsed
        except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError):
            pass
        # fallback placeholder schedule
        return {
            "fajr": "05:00",
            "dhuhr": "12:10",
            "asr": "15:30",
            "maghrib": "17:45",
            "isha": "19:15",
        }

    def _extract_schedule(self, payload: object, target_date: date) -> Dict[str, str]:
        """Handle the handful of structures returned by the API."""
        if not payload:
            return {}

        if isinstance(payload, dict):
            data_section = payload.get("data")
            if isinstance(data_section, dict) and "Prayer" in data_section:
                return self._normalize_prayer_map(data_section.get("Prayer"))
            if isinstance(data_section, Iterable):
                return self._find_schedule_in_iterable(data_section, target_date)
            # Sometimes payload itself is already a list of days
            if "Prayer" in payload:
                return self._normalize_prayer_map(payload.get("Prayer"))

        if isinstance(payload, Iterable):
            return self._find_schedule_in_iterable(payload, target_date)
        return {}

    def _find_schedule_in_iterable(self, data: Iterable[object], target_date: date) -> Dict[str, str]:
        """Search through iterable API data for a specific date entry."""
        for entry in data:
            if not isinstance(entry, dict):
                continue
            date_value = entry.get("Date") or entry.get("date") or entry.get("prayer_date")
            if date_value and str(target_date.day) in str(date_value):
                prayer_values = (
                    entry.get("Prayer")
                    or entry.get("PrayerTiming")
                    or {k: v for k, v in entry.items() if k.lower() in self._prayer_keys()}
                )
                return self._normalize_prayer_map(prayer_values)
        return {}

    def _normalize_prayer_map(self, raw: object) -> Dict[str, str]:
        if not isinstance(raw, dict):
            return {}
        normalized: Dict[str, str] = {}
        for key, value in raw.items():
            if not isinstance(value, str):
                continue
            normalized[key.lower()] = value
        return normalized

    @staticmethod
    def _prayer_keys() -> Iterable[str]:
        return ("fajr", "dhuhr", "asr", "maghrib", "isha")
