"""Constrain runtime file access to the explicitly selected repository."""

import json
from pathlib import Path


def inside(root: Path, relative: str | Path) -> Path:
    """Resolve a project-relative path and reject traversal and symlink escapes."""
    relative = Path(relative)
    if relative.is_absolute():
        raise ValueError("Resource paths must stay inside the selected repository")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Resource paths must stay inside the selected repository")
    return path


def read_json(path: Path) -> dict:
    """Read a JSON object, rejecting catalogs with another top-level shape."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")
    return data
