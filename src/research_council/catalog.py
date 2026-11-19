"""Local lexical retrieval from approved, integrity-checked source snapshots."""

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from .paths import inside, read_json

EXPERTS = (
    "technology-evolution",
    "sexual-selection",
    "natural-selection",
    "cultural-evolution",
    "angel-investment",
    "venture-capital",
)
CATALOGS = ("contexts/resources/catalog.json", "contexts/resources/catalog.web.json")
MAX_SOURCE_BYTES = 5 * 1024 * 1024


def check_expert(expert: str) -> None:
    if expert not in EXPERTS:
        raise ValueError("Unknown expert")


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    owner: str
    raw_path: str
    sha256: str
    text_path: str
    text_sha256: str
    secondary: tuple[str, ...]


@dataclass(frozen=True)
class Passage:
    source_id: str
    title: str
    path: str
    start_line: int
    end_line: int
    text: str
    score: int
    raw_sha256: str
    text_sha256: str
    truncated: bool = False


class Catalog:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.records: dict[str, Source] = {}
        for relative in CATALOGS:
            path = inside(self.root, relative)
            if not path.exists():
                continue
            for record in read_json(path)["records"]:
                source = self._source(record)
                if source.id in self.records:
                    raise ValueError(f"Duplicate source ID: {source.id}")
                self.records[source.id] = source

    def _source(self, record: dict) -> Source:
        check_expert(record["owner"])
        for key in ("raw_path", "text_path"):
            inside(self.root, record.get(key, record["raw_path"]))
        if not re.fullmatch(r"[A-Z][A-Z0-9_-]{1,63}", record["id"]):
            raise ValueError("Invalid source ID")
        return Source(
            record["id"],
            record["title"],
            record["owner"],
            record["raw_path"],
            record["sha256"],
            record.get("text_path", record["raw_path"]),
            record.get("text_sha256", record["sha256"]),
            tuple(record.get("secondary", [])),
        )

    def sources(self, expert: str, *, include_secondary: bool = False) -> list[Source]:
        check_expert(expert)
        mapping = read_json(inside(self.root, f"contexts/resources/{expert}/context-map.json"))
        primary = set(mapping.get("primary_note_ids", []) + mapping.get("primary_source_ids", []))
        secondary = set(mapping.get("secondary_note_ids", [])) if include_secondary else set()
        return sorted(
            (
                s
                for s in self.records.values()
                if (s.id in primary and s.owner == expert)
                or (s.id in secondary and expert in s.secondary)
            ),
            key=lambda s: s.id,
        )

    def text(self, source: Source) -> str:
        """Verify both raw and extracted bytes before returning searchable text."""
        for relative, expected in (
            (source.raw_path, source.sha256),
            (source.text_path, source.text_sha256),
        ):
            path = inside(self.root, relative)
            if path.stat().st_size > MAX_SOURCE_BYTES:
                raise ValueError(f"Source exceeds size limit: {source.id}")
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError(f"Source integrity mismatch: {source.id}")
        return inside(self.root, source.text_path).read_text(encoding="utf-8")

    def verify(self) -> int:
        for source in self.records.values():
            self.text(source)
        return len(self.records)

    def search(
        self, expert: str, query: str, *, limit: int = 3, include_secondary: bool = False
    ) -> list[Passage]:
        check_expert(expert)
        terms = tuple(dict.fromkeys(re.findall(r"[^\W_]+", query.casefold())))
        if not terms or len(query) > 4000 or not 1 <= limit <= 10:
            raise ValueError("Provide a nonempty query up to 4000 characters and limit 1–10")
        patterns = [
            re.compile(r"\b" + re.escape(t) + r"\b") if t.isascii() else re.compile(re.escape(t))
            for t in terms
        ]
        hits = []
        for source in self.sources(expert, include_secondary=include_secondary):
            lines = self.text(source).splitlines()
            for offset in range(0, len(lines), 40):
                chunk = lines[offset : offset + 40]
                scores = [sum(len(p.findall(line.casefold())) for p in patterns) for line in chunk]
                if sum(scores):
                    first = next(i for i, score in enumerate(scores) if score)
                    excerpt = "\n".join(chunk[first:])
                    truncated = len(excerpt) > 2400
                    excerpt = excerpt[:2400]
                    end = offset + first + len(excerpt.splitlines())
                    hits.append(
                        Passage(
                            source.id,
                            source.title,
                            source.text_path,
                            offset + first + 1,
                            end,
                            excerpt,
                            sum(scores),
                            source.sha256,
                            source.text_sha256,
                            truncated,
                        )
                    )
        return sorted(hits, key=lambda h: (-h.score, h.source_id, h.start_line))[:limit]
