# Development and validation

## Local checks

```sh
uv sync --locked --dev
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest --cov=research_council --cov-report=term-missing
```

Tests require no private corpus, API keys, network calls, or server. Coverage has an 80% minimum. They cover source boundaries, hashes, isolated contexts, import rollback/locking, redaction, budgets, failures, retrieval, and avoiding network calls with inherited tracing flags. Integration tests generate a workspace at runtime.

The user runs and restarts services. Do not launch a server as a development check.

## Dependencies

Use uv.lock for reproducibility. Dependencies are in pyproject.toml; test/lint tools are in the dev group. Updates should regenerate the lock, run checks, and explain compatibility effects.

LangGraph runs locally. LangSmith is transitive, but hosted tracing is disabled inside preparation. OpenTelemetry uses a local exporter. No framework subscription or remote observability account is required.

## GitHub Actions

The prepared workflow runs on pushes, pull requests, and manual dispatch. It has read-only repository permissions, does not persist checkout credentials, and needs no secrets. It installs locked dependencies, checks lint/formatting, runs coverage, and builds distributions locally.

It does not publish packages, deploy infrastructure, restore private data, upload reports, or run model research.

Action pins and uv integration were checked against the [official uv GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/). CI selects Python 3.12 and uv 0.9.7, matching the initial local toolchain.

## Packaging

```sh
uv build
```

This creates local archives under ignored dist/. It does not publish them. The wheel contains the application package. The source archive uses an explicit inclusion list so private libraries, credentials, agent configuration, caches, and reports are not picked up by a broad scan.

Inspect archive members before distribution. Update the explicit list when adding a public document or example. A license still needs to be selected; see [NOTICE](../NOTICE.md).

## Optional documentation tools

Ref can help coding agents search documentation, but is not required by the application or CI. Keep its MCP setup and authentication outside this repository. Use official library/provider documentation and validate against the pinned installed package.

Developer documentation and project research sources are separate libraries. An installed tool on one machine is not automatically available in a clean checkout.
