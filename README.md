# Agent Syndicate

Agent Syndicate is a CLI framework for bottom-up investment research informed by evolutionary principles. Start with evidence about a specific technology, customer behavior, or company. Use evolutionary ideas such as variation, selection, and recombination to surface hypotheses, then test them against alternative explanations. The framework prepares separate evidence packets so specialist perspectives can be compared.

**Current status:** working local source import, integrity checks, expert-specific search, and bounded context preparation. Live model research, agent debate, TiDB, Filesystem/Drive9, and mem9 adapters are still planned. No UI or server is required.

## Quick start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run these commands from the repository root:

```sh
uv sync --locked
uv run council --help
uv run pytest
```

The tests exercise the preparation workflow with temporary data. For research, [configure a private workspace](docs/SOURCES.md) with your own expert rules, charters, and sources, then run:

```sh
uv run council --root .local/workspace doctor
uv run council --root .local/workspace prepare --topic 'What changed to make this market viable?'
```

Preparation writes six source packets, a Markdown brief, a provenance manifest, and local OpenTelemetry traces under the selected workspace's runs directory. The output status is `prepared_not_researched`.


## The six roles

| Expert | Question |
| --- | --- |
| Technology evolution | What components, prerequisites, and combinations make a new capability possible? |
| Sexual selection | Could preferences and displays help explain demand, and what alternatives fit? |
| Natural selection | What varies, gets transmitted, and is selected? Where does the analogy fail? |
| Cultural evolution | Who learns what from whom, and why does the practice persist or spread? |
| Angel investment | What can a team establish before the next commitment of capital? |
| Venture capital | Can a company scale and capture value at plausible financing and entry conditions? |

Context files do not fine-tune models. The design keeps source arguments, empirical findings, user interpretations, and new hypotheses distinguishable. Technology growth, company value capture, and investor returns are separate questions.

## Configuration

**Nothing needs to be configured for the tests.** The blank [.env.example](.env.example) documents future settings. Keep real credentials in the selected private workspace's ignored `.env`.

| Component | Current behavior |
| --- | --- |
| Python and uv | Python 3.12 selected; dependencies pinned in uv.lock |
| LangGraph | Local open-source workflow; no paid hosted platform required |
| Models | No default provider or model; live calls not implemented |
| OpenTelemetry | Local JSONL spans; remote export not implemented |
| LangSmith | Upstream dependency; hosted tracing explicitly disabled |
| TiDB Starter | Future structured state and checkpoints |
| Filesystem / Drive9 | Future durable source/artifact storage |
| mem9 | Future private expert spaces and controlled shared memory |
| Ref | Optional developer documentation tool; not an application dependency |

See [configuration](docs/CONFIGURATION.md) for all 29 environment variables and their implementation status. Populating a key does not activate an unfinished feature.

## Repository layout

```text
src/research_council/       CLI, configuration, retrieval, import, workflow, telemetry
tests/                     Offline tests and isolation checks
docs/                      Setup, configuration, architecture, sources, roadmap
.github/                   CI and pull-request template
.env.example               Blank configuration reference
pyproject.toml              Package metadata and test/lint/build configuration
uv.lock                    Reproducible dependency resolution
```

Personal notes, derived personal research context, source archives, authentication files, caches, and generated reports are excluded from the shared tree. Existing local research files remain in place. Use a separate ignored workspace for real material; see [source management](docs/SOURCES.md).

## Development

```sh
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest --cov=research_council --cov-report=term-missing
```

CI runs these checks on GitHub. It requires no repository secrets, starts no servers, and does not publish packages or deploy services.

## Documentation

Start with the [documentation index](docs/README.md), [setup guide](docs/SETUP.md), and [implementation status](docs/IMPLEMENTATION_STATUS.md). Read the [architecture](docs/ARCHITECTURE.md), [roadmap](docs/ROADMAP.md), and [GitHub preparation notes](docs/GITHUB_PREPARATION.md) for the remaining work and publication boundaries.

See [contributing](CONTRIBUTING.md), [security](SECURITY.md), and [code/source licensing](NOTICE.md). A license has not been selected.
