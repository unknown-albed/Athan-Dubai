"""Configuration helpers for DubaiAthan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG = {
    "api": {
        "base_url": "https://api-crm.iacad.gov.ae/api//prayertime/getprayerfromlink",
        "timeout": 10,
    },
    "location": {"city_id": 1, "timezone": "Asia/Dubai"},
    "ui": {"theme": "desert"},
}


def load_config(config_path: Path | None = None) -> Dict[str, Any]:
    """Load configuration from disk, falling back to defaults."""
    path = config_path or Path(__file__).resolve().parents[1] / "config.json"
    if not path.exists():
        return DEFAULT_CONFIG.copy()

    try:
        with path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_CONFIG.copy()

    # Merge shallowly with defaults to ensure required keys are present.
    merged = DEFAULT_CONFIG.copy()
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(DEFAULT_CONFIG.get(key), dict):
            merged[key] = {**DEFAULT_CONFIG[key], **value}
        else:
            merged[key] = value
    return merged
