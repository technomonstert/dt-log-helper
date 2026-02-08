"""Utility functions for file I/O, handling UTF‑8‑BOM, and simple validation.
"""

import json
from pathlib import Path

def read_json(file_path: str) -> dict:
    """Read a JSON file using UTF‑8‑BOM handling.
    Returns the parsed dict or raises a helpful exception.
    """
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as exc:
        raise Exception(f"Failed to read JSON file '{file_path}': {exc}")
