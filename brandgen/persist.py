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


def load_isic_groups(path: str) -> Dict[str, Dict[str, str]]:
    """Load ISIC groups from flattened CSV file.
    
    Returns dict mapping group_name -> {section_name, division_name, group_name, includes, excludes}
    """
    import csv
    groups = {}
    
    try:
        with Path(path).open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                group_name = row.get("group_name", "").strip()
                if group_name:  # Only process rows with group names
                    groups[group_name] = {
                        "section_name": row.get("section_name", "").strip(),
                        "division_name": row.get("division_name", "").strip(), 
                        "group_name": group_name,
                        "includes": row.get("includes", "").strip(),
                        "excludes": row.get("excludes", "").strip(),
                    }
    except FileNotFoundError:
        raise FileNotFoundError(f"ISIC flattened file not found at {path}")
    except Exception as e:
        raise ValueError(f"Error reading ISIC flattened file: {e}")
    
    return groups
