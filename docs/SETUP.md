# Setup and CLI use

## Requirements

Python 3.11 or newer is required; Python 3.12 is selected in .python-version and used for validation. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for the locked environment. Internet access is needed for the initial dependency installation. The tests need no model API or cloud account.

From the repository root:

```sh
uv sync --locked
uv run council --help
```

Create a [private workspace](SOURCES.md) for research commands.

## Commands

| Command | Behavior |
| --- | --- |
| `doctor` | Verify catalogue hashes and report redacted configuration readiness |
| `sources list --expert <id>` | List the selected expert's primary sources |
| `sources search --expert <id> --query <text>` | Retrieve local passages with source IDs, locators, hashes, and scores |
| `sources import-html <file> ...` | Import approved HTML already downloaded inside the selected workspace |
| `prepare --topic <text>` | Produce six bounded context packets and a preparation brief without model calls |
| `run --topic <text>` | Exit with an explicit explanation: live research is not implemented |

`--root` belongs before the command. It selects the data workspace; the application package remains installed from this repository.

```sh
uv run council --root .local/workspace sources list --expert angel-investment
uv run council --root .local/workspace sources search --expert technology-evolution --query recombination
uv run council --root .local/workspace prepare --topic 'recombination adoption'
```

The installed entry points also work through `.venv/bin/council` or `.venv/bin/python -m research_council` on macOS/Linux. On Windows, uv manages the platform-specific environment paths.

## Retrieval and context limits

Search is lexical, not semantic. English words use boundaries; Chinese terms use substring matching. Queries have a 4,000-character limit. `--limit` accepts 1–10 passages, with three by default. Excerpts have a truncation flag and cite actual source lines.

Primary sources are isolated by expert. `--include-secondary` explicitly adds approved neighboring sources for list/search; it does not merge charters or memories. Preparation currently retrieves primary sources only.

`prepare --context-chars 24000` sets the per-expert character ceiling; this is not a token estimate. Complete shared rules and the expert's charter must fit before excerpts are added. Too-small budgets fail before a run is created. Missing matches remain visible.

## Output

All output goes inside the selected workspace:

```text
runs/<UTC timestamp>-<random suffix>/
  brief.md
  manifest.json
  traces.jsonl
  contexts/
    technology-evolution.md
    sexual-selection.md
    natural-selection.md
    cultural-evolution.md
    angel-investment.md
    venture-capital.md
```

Open brief.md in a Markdown reader. `prepared_not_researched` means source packets and instructions, not findings, forecasts, debate, or investment recommendations. The manifest records source and context hashes. Failed workflows have FAILED.txt and no completed manifest.

## Your own sources

Use an ignored private workspace as described in [source management](SOURCES.md). Copy the blank environment template into that selected root only if needed. Existing owner workspaces can still use the repository root explicitly; reorganization does not move or remove their notes.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Invalid project path or missing files | Set `--root` to a configured private workspace. |
| Source integrity failure | Check raw/extracted bytes against catalogue hashes. Do not silently change hashes to bypass validation. |
| Empty search results | Use words present in a source and the correct expert. Retrieval does not infer synonyms. |
| Import already exists | Use a new ID/version rather than overwrite an archive. |
| Import lock remains | Check active importers and interrupted writes before removing contexts/resources/.import.lock. |
| Context budget too small | Increase it enough to preserve the rules and charter. |
| `run` exits with an explanation | Expected: model research and debate remain pending. Use `prepare`. |
| uv cache access fails in a sandbox | Try `UV_CACHE_DIR=.cache/uv`; a macOS sandbox can also block uv's system-configuration probe, requiring normal terminal execution. |

The user runs or restarts services. No application server is needed for these commands.

[Configuration](CONFIGURATION.md) · [Development](DEVELOPMENT.md) · [Implementation status](IMPLEMENTATION_STATUS.md)
