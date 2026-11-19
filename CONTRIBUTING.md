# Contributing

Start with [setup](docs/SETUP.md), [architecture](docs/ARCHITECTURE.md), and [implementation status](docs/IMPLEMENTATION_STATUS.md). The current program prepares source-backed expert inputs; it does not perform live agent research.

## Development

```sh
uv sync --locked --dev
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest --cov=research_council --cov-report=term-missing
```

Tests create isolated temporary workspaces. No API keys, paid calls, private corpus, or running server are required.

Keep changes focused. Explain what changed, why it matters, and how it was validated. Add meaningful tests for new behavior and regressions; do not write tests that merely restate documentation. Update the appropriate configuration and status docs when a feature becomes usable.

## Boundaries

Do not commit private notes, source archives, generated reports, credentials, or account configuration. A private GitHub repository still shares material with everyone who has access; do not force-add ignored files to bypass the source boundaries.

Keep source arguments, empirical findings, user interpretations, and new hypotheses distinct. Include access limitations and source lineage. Synthetic examples are illustrations, not evidence. A model's agreement with another model is not independent corroboration.

The user controls services and publication. Contributors should not start servers, provision cloud resources, push branches, or publish artifacts without authorization. See [security](SECURITY.md) and [source management](docs/SOURCES.md).
