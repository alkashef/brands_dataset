"""Persistence helpers.

Responsibility: Minimal JSON file IO plus industries sections loader.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: str) -> Any:
    """Load and return JSON content from a file path."""
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: str, data: Any) -> None:
    """Persist Python data structure as pretty JSON to disk."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def load_sections(path: str) -> Dict[int, str]:
    """Return mapping of section index -> label from industries JSON."""
    payload = load_json(path)
    sections = payload.get("sections", {}) if isinstance(payload, dict) else {}
    return {int(k): v for k, v in sections.items()}


def load_companies(path: str) -> Dict[str, List[Dict[str, str]]]:
    """Load previously generated companies JSON (section label -> list of company dicts)."""
    data = load_json(path)
    return data if isinstance(data, dict) else {}
