"""Terminal entry point. Network integrations are deliberately not implicit."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from .catalog import EXPERTS, Catalog
from .configuration import Settings
from .ingest import import_html
from .workflow import prepare


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(prog="council")
    cli.add_argument("--root", type=Path, default=Path.cwd(), help="Explicit repository root")
    commands = cli.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Check source integrity and redacted configuration")
    sources = commands.add_parser("sources").add_subparsers(dest="action", required=True)
    listing = sources.add_parser("list")
    search = sources.add_parser("search")
    for child in (listing, search):
        child.add_argument("--expert", choices=EXPERTS, required=True)
        child.add_argument("--include-secondary", action="store_true")
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=3)
    ingest = sources.add_parser("import-html", help="Import already-downloaded HTML inside root")
    ingest.add_argument("file", type=Path)
    ingest.add_argument("--id", dest="source_id", required=True)
    ingest.add_argument("--expert", choices=EXPERTS, required=True)
    for field in ("url", "title", "author", "published"):
        ingest.add_argument(f"--{field}", required=True)
    draft = commands.add_parser("prepare", help="Create six source packets without model calls")
    draft.add_argument("--topic", required=True)
    draft.add_argument("--context-chars", type=int, default=24000)
    live = commands.add_parser("run", help="Reserved live-research command; fails explicitly")
    live.add_argument("--topic", required=True)
    return cli


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "doctor":
            settings = Settings.load(root)
            catalog = Catalog(root)
            result = dict(
                settings.status(),
                sources=catalog.verify(),
                experts={e: len(catalog.sources(e)) for e in EXPERTS},
            )
        elif args.command == "prepare":
            result = {
                "output": str(prepare(root, args.topic, context_chars=args.context_chars)),
                "status": "prepared_not_researched",
            }
        elif args.command == "run":
            Settings.load(root).require_live()
        else:
            result = _sources(args, root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        # Never echo exception details that might contain a credential or raw JSON source body.
        message = (
            "Live research is not implemented; use prepare."
            if args.command == "run"
            else "Invalid configuration, source integrity, input, or project path. "
            "Check the command arguments and local files."
        )
        print(f"council: {message}", file=sys.stderr)
        return 2


def _sources(args, root: Path):
    if args.action == "import-html":
        return import_html(
            root,
            args.file,
            source_id=args.source_id,
            expert=args.expert,
            url=args.url,
            title=args.title,
            author=args.author,
            published=args.published,
        )
    catalog = Catalog(root)
    if args.action == "list":
        return [
            asdict(s)
            for s in catalog.sources(args.expert, include_secondary=args.include_secondary)
        ]
    return [
        asdict(hit)
        for hit in catalog.search(
            args.expert, args.query, limit=args.limit, include_secondary=args.include_secondary
        )
    ]
