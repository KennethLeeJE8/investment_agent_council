# Implementation status

Updated 15 November 2026. The repository has executable local preparation code. It does not yet run the full research council.

| Capability | Status |
| --- | --- |
| Package, CLI entry point, locked dependencies | Implemented |
| Blank dotenv configuration, precedence, redacted status | Implemented |
| Local source hashes and path boundaries | Implemented |
| Primary isolation and explicit secondary search | Implemented |
| English/Chinese lexical retrieval and line citations | Implemented |
| HTML archive, extraction, provenance, locking/rollback | Implemented |
| Six separate bounded source packets and Markdown brief | Implemented through LangGraph |
| Context and source hashes in the run manifest | Implemented |
| OpenTelemetry local span metadata | Implemented; remote export deferred |
| Hosted LangSmith tracing | Explicitly disabled in the workflow |
| Offline tests | Temporary fixtures exercise source preparation without a private corpus or keys |
| GitHub CI configuration | Prepared locally; no remote workflow run is claimed |
| Provider calls and independent expert research | Not implemented |
| Evidence review, discussion, revision, synthesis | Planned |
| TiDB Starter, Filesystem/Drive9, mem9 | Planned |
| Durable checkpoint/resume | Planned |
| Production source libraries | User-managed private data, excluded from the shared repository |

Local validation: 38 tests passed with approximately 96% line coverage. The same 38 tests passed from a copy of only the proposed shared files, without the personal library. Lint, formatting, clean-copy preparation, and archive content checks passed. GitHub-hosted CI has not been run. Synthetic examples do not validate scientific reasoning or investment performance.

No server, model key, cloud deployment, GitHub secret, or Ref installation is required for preparation and tests. [Configuration](CONFIGURATION.md) distinguishes readiness fields from working integrations.

[Setup](SETUP.md) · [Roadmap](ROADMAP.md) · [GitHub preparation](GITHUB_PREPARATION.md)
