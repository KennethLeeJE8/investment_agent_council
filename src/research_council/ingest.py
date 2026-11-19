"""Import user-approved, already-downloaded HTML without fetching other URLs."""

import hashlib
import json
import os
import re
import shutil
import tempfile
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

from .catalog import MAX_SOURCE_BYTES, Catalog, check_expert
from .paths import inside, read_json


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def _atomic_bytes(path: Path, data: bytes) -> None:
    fd, temp = tempfile.mkstemp(prefix=".import-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temp, path)
    finally:
        Path(temp).unlink(missing_ok=True)


def import_html(
    root: Path,
    html_path: Path,
    *,
    source_id: str,
    expert: str,
    url: str,
    title: str,
    author: str,
    published: str,
) -> dict:
    """Archive raw HTML plus normalized text and register one primary expert."""
    root = root.resolve()
    check_expert(expert)
    if not re.fullmatch(r"[A-Z][A-Z0-9_-]{1,63}", source_id):
        raise ValueError("Invalid source ID")
    parsed = urlsplit(url)
    if (
        parsed.scheme not in ("https", "http")
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError("Source URL must be HTTP(S) metadata without credentials")
    if any(
        not value.strip() or len(value) > 500 or "\n" in value
        for value in (title, author, published)
    ):
        raise ValueError("Provide short, single-line title, author, and publication date")
    html_path = inside(root, html_path.relative_to(root) if html_path.is_absolute() else html_path)
    if html_path.stat().st_size > MAX_SOURCE_BYTES:
        raise ValueError("HTML exceeds the 5 MiB source limit")
    raw = html_path.read_bytes()
    soup = BeautifulSoup(raw, "html.parser")
    for element in soup(["script", "style", "noscript"]):
        element.decompose()
    text = (soup.body or soup).get_text("\n", strip=True) + "\n"
    if not text.strip():
        raise ValueError("HTML contains no readable text")
    return _commit_import(
        root,
        source_id,
        expert,
        raw,
        text,
        {
            "title": title,
            "author": author,
            "published": published,
            "url": url,
            "retrieved_at": datetime.now(UTC).isoformat(),
            "kind": "investor_essay",
            "read_status": "full_essay_text_available",
            "origin": "source argument; not verified empirical evidence",
        },
    )


@contextmanager
def _import_lock(root: Path):
    lock = inside(root, "contexts/resources/.import.lock")
    try:
        lock.touch(exist_ok=False)
    except FileExistsError as exc:
        raise ValueError("Another import is in progress; inspect .import.lock") from exc
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)


def _commit_import(
    root: Path, source_id: str, expert: str, raw: bytes, text: str, metadata: dict
) -> dict:
    # Lock before reading metadata to prevent concurrent imports losing each other's updates.
    with _import_lock(root):
        return _write_import(root, source_id, expert, raw, text, metadata)


def _write_import(
    root: Path, source_id: str, expert: str, raw: bytes, text: str, metadata: dict
) -> dict:
    catalog = Catalog(root)
    base = inside(root, f"contexts/resources/{expert}/raw/{source_id}")
    if source_id in catalog.records or base.exists():
        raise ValueError(f"Source already exists: {source_id}")
    web_path = inside(root, "contexts/resources/catalog.web.json")
    map_path = inside(root, f"contexts/resources/{expert}/context-map.json")
    web = read_json(web_path) if web_path.exists() else {"schema_version": 1, "records": []}
    mapping = read_json(map_path)
    record = dict(
        metadata,
        id=source_id,
        owner=expert,
        secondary=[],
        raw_path=f"contexts/resources/{expert}/raw/{source_id}/source.html",
        text_path=f"contexts/resources/{expert}/raw/{source_id}/source.txt",
        sha256=hashlib.sha256(raw).hexdigest(),
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
        words=len(text.split()),
        lines=len(text.splitlines()),
    )
    web["records"].append(record)
    mapping["primary_source_ids"] = mapping.get("primary_source_ids", []) + [source_id]
    mapping["status"] = "specialist_corpus_seeded"
    backups = {p: p.read_bytes() if p.exists() else None for p in (web_path, map_path)}
    try:
        base.mkdir(parents=True)
        (base / "source.html").write_bytes(raw)
        (base / "source.txt").write_text(text, encoding="utf-8")
        _atomic_bytes(web_path, _json_bytes(web))
        _atomic_bytes(map_path, _json_bytes(mapping))
    except Exception:
        for path, previous in backups.items():
            if previous is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(previous)
        shutil.rmtree(base, ignore_errors=True)
        raise
    return record
