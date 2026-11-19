# Configuration

No credentials are required for tests, local source import/search, or context preparation. The complete template is [.env.example](../.env.example); all values are intentionally empty.

The CLI reads `.env` inside the root selected by `--root`, then applies process environment values on top. Running against a private workspace reads that workspace’s `.env`. Dotenv values are not shell commands and are not expanded through variable interpolation.

For your own ignored workspace, copy the template into that workspace as `.env`. Fill only settings you intend to configure. `doctor` reports booleans, never credentials. Its readiness flags are not connectivity tests, account-eligibility checks, or proof that an adapter exists.

## Model settings — deferred

| Variable | Intended role |
| --- | --- |
| `COUNCIL_MODEL_PROVIDER` | Provider selector. Current configuration checks recognize `openai`, `anthropic`, `moonshot`, and `deepseek`; this does not implement their API adapters. |
| `COUNCIL_MODEL_NAME` | Explicit model identifier, with no default. |
| `COUNCIL_MODEL_BASE_URL` | Optional future endpoint override; not consumed by a live client yet. |
| `OPENAI_API_KEY` | Future OpenAI provider credential. |
| `ANTHROPIC_API_KEY` | Future Anthropic provider credential. |
| `MOONSHOT_API_KEY` | Future Moonshot provider credential. |
| `DEEPSEEK_API_KEY` | Future DeepSeek provider credential. |

Leave these empty now. The `run` command refuses live research even if credentials are populated. No subscription login, default model, or paid fallback is invoked. Model availability and regional access must be checked when the provider adapter is implemented.

## TiDB Starter — deferred

| Variable | Intended role |
| --- | --- |
| `TIDB_HOST` | Database hostname. |
| `TIDB_PORT` | Explicit port when needed by the future connector. |
| `TIDB_DATABASE` | Application database. |
| `TIDB_USER` | Least-privilege application user. |
| `TIDB_PASSWORD` | User password. |
| `TIDB_SSL_CA` | Trusted certificate path, if required by the selected connector. |

The future adapter will store structured research records and checkpoints. No driver connects, migrations run, or cloud resources are created by the current CLI. Database protocol, region, schema, TLS behavior, and connectivity still need validation.

## TiDB Filesystem / Drive9 — deferred

| Variable | Intended role |
| --- | --- |
| `TIDB_FILESYSTEM_URL` | Regional filesystem endpoint. |
| `TIDB_FILESYSTEM_ID` | Target filesystem identity. |
| `TIDB_FILESYSTEM_TOKEN` | Filesystem-specific access token. |

This future layer will retain source snapshots and research artifacts. It is separate from database credentials. No files are uploaded today.

## mem9 — deferred

| Variable | Intended role |
| --- | --- |
| `MEM9_API_URL` | Memory API origin. |
| `MEM9_TECHNOLOGY_EVOLUTION_API_KEY` | Technology expert's private space. |
| `MEM9_SEXUAL_SELECTION_API_KEY` | Sexual-selection expert's private space. |
| `MEM9_NATURAL_SELECTION_API_KEY` | Natural-selection expert's private space. |
| `MEM9_CULTURAL_EVOLUTION_API_KEY` | Cultural-evolution expert's private space. |
| `MEM9_ANGEL_INVESTMENT_API_KEY` | Angel expert's private space. |
| `MEM9_VENTURE_CAPITAL_API_KEY` | VC expert's private space. |
| `MEM9_SHARED_API_KEY` | Controlled publication space for reviewed shared findings. |

The intended design keeps expert memories separate. A shared key is not a substitute for every expert's own space. No memory API calls, automatic source ingestion, or shared-memory publication occur today.

## Research search — deferred

| Variable | Intended role |
| --- | --- |
| `RESEARCH_SEARCH_PROVIDER` | Future research-search service selector. |
| `RESEARCH_SEARCH_API_KEY` | Search-service credential. |
| `RESEARCH_SEARCH_BASE_URL` | Future service endpoint. |

These do not affect current local lexical retrieval. No web research is performed by `prepare`.

## Observability

| Variable | Current behavior |
| --- | --- |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Reserved for a future optional exporter; ignored by the current local exporter. |
| `OTEL_EXPORTER_OTLP_HEADERS` | Reserved exporter authentication; never printed by configuration checks. |

OpenTelemetry currently writes span metadata to the selected run's traces.jsonl. Topics, prompts, keys, and raw source content are not span attributes. The workflow explicitly disables hosted LangSmith tracing, even when tracing flags are inherited. LangSmith is an upstream dependency, not a required account or paid service.

## GitHub and optional tools

CI needs no repository secrets or model keys. Publishing, deployments, and cloud provisioning are not configured. Ref is an optional developer documentation tool, configured outside this application. Its authentication, any coding subscription, and model-provider API keys are separate settings; none belong in Git.
