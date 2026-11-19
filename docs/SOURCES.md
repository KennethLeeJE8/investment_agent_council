# Source libraries and private workspaces

Choose a private workspace such as `.local/workspace`, which Git ignores. Create the directories below and supply your own shared rules and one charter for each expert listed in the README. Start `catalog.json` with `{"records": []}` and each `context-map.json` with `{"primary_note_ids": [], "secondary_note_ids": []}`. The environment file is optional.

Once the workspace is in place, run `uv run council --root .local/workspace doctor`. Import approved sources before preparing your first evidence packets.

## Required structure

```text
<workspace>/
  .env                          optional, private
  contexts/
    SHARED_RESEARCH_RULES.md
    experts/<expert-id>.md
    resources/
      catalog.json
      catalog.web.json          optional until HTML is imported
      <expert-id>/context-map.json
      <expert-id>/raw/          private source archives
  runs/                         generated private output
```

Catalogue paths are relative to the workspace, not the original notes collection. IDs must be unique. Each source has one primary owner and a SHA-256. When searchable text differs from raw HTML, both have hashes. Secondary access requires a matching map and source route.

The CLI reads only the selected workspace. Paths outside it, including symlink escapes, are rejected. Original note collections need not remain accessible after snapshots are admitted.

## Import an approved essay

Download the approved URL through an authorized ingestion step, save it inside the workspace, then import it:

```sh
uv run council --root .local/workspace sources import-html downloads/approved.html \
  --id WEB001 --expert angel-investment \
  --url 'https://author.example/essay' \
  --title 'Essay title' --author 'Author name' --published 'YYYY-MM'
```

The command preserves raw bytes, extracts text without executing scripts, and registers the source in the web catalogue and one expert's map. It does not fetch links, create a scientific summary, or assert a human has read the material. The limit is 5 MiB per source. Existing IDs are not overwritten.

After reading, add a guide distinguishing the author's position, your interpretation, and new hypotheses. Record publication date, stage/geography where relevant, evidence type, access depth, limitations, and counterarguments. Preserve footnotes. Repeated notes about one study are not independent corroboration.

## Distinct expert contexts

Load shared rules, the topic, the expert's charter, and relevant passages. Do not inject the whole library or every expert's opinions into each call. Peer requests should identify a claim, locators, uncertainty, and a discriminating question.

Biological inheritance, developmental plasticity, individual learning, cultural transmission, deliberate engineering, and analogy need separate explanations. Popularity, adoption, company revenue, and investor return are different outcomes.

## Backup and cloud publication

Back up private workspaces separately, including raw files, catalogues, maps, charters, guides, and needed reports. Hashes detect changes but cannot restore missing content. Original note collections remain read-only unless separately authorized.

No cloud ingestion is implemented. Future TiDB, Filesystem/Drive9, or mem9 adapters need explicit data scope, configured destinations, and provenance. Keep raw documents separate from reviewed memory and private spaces separate from shared publication. See [configuration](CONFIGURATION.md) and [licensing](../NOTICE.md).
