import hashlib
import json

import pytest

from research_council.catalog import Catalog
from research_council.ingest import import_html


def ingest(workspace, source_id="AI001", url="https://example.com/essay"):
    source = workspace / "download.html"
    source.write_bytes(
        b"<html><body><h1>Essay</h1><p>Founder resourcefulness.</p>"
        b"<script>steal secrets</script><style>hidden</style><p>Notes</p>"
        b"<p>[1] A complete footnote.</p></body></html>"
    )
    return import_html(
        workspace,
        source,
        source_id=source_id,
        expert="angel-investment",
        url=url,
        title="Essay",
        author="Example",
        published="2009-03",
    )


def test_import_preserves_raw_and_searches_text_including_notes(workspace):
    record = ingest(workspace)
    assert (workspace / record["raw_path"]).read_bytes() == (
        workspace / "download.html"
    ).read_bytes()
    text = (workspace / record["text_path"]).read_text()
    assert "complete footnote" in text
    assert "steal secrets" not in text and "hidden" not in text
    assert (
        hashlib.sha256((workspace / record["raw_path"]).read_bytes()).hexdigest()
        == record["sha256"]
    )
    assert Catalog(workspace).search("angel-investment", "resourcefulness")[0].source_id == "AI001"


@pytest.mark.parametrize(
    "source_id,url",
    [
        ("../escape", "https://example.com"),
        ("AI001", "file:///etc/passwd"),
        ("AI001", "https://user:password@example.com"),
        ("AI001", "https://:password@example.com"),
    ],
)
def test_bad_metadata_leaves_no_import(workspace, source_id, url):
    with pytest.raises(ValueError):
        ingest(workspace, source_id, url)
    assert not (workspace / "contexts/resources/catalog.web.json").exists()


def test_reimport_does_not_overwrite(workspace):
    ingest(workspace)
    before = (workspace / "contexts/resources/catalog.web.json").read_bytes()
    with pytest.raises(ValueError, match="exists"):
        ingest(workspace)
    assert (workspace / "contexts/resources/catalog.web.json").read_bytes() == before


def test_bad_existing_catalog_does_not_leave_new_files(workspace):
    ingest(workspace)
    p = workspace / "contexts/resources/catalog.web.json"
    p.write_text("broken JSON")
    with pytest.raises(ValueError):
        ingest(workspace, "AI002")
    assert not (workspace / "contexts/resources/angel-investment/raw/AI002").exists()


def test_import_registers_only_own_expert(workspace):
    ingest(workspace)
    folder = workspace / "contexts/resources"
    angel = json.loads((folder / "angel-investment/context-map.json").read_text())
    vc = json.loads((folder / "venture-capital/context-map.json").read_text())
    assert "AI001" in angel["primary_source_ids"]
    assert "AI001" not in vc.get("primary_source_ids", [])


def test_write_failure_rolls_back_catalog_and_map(workspace, monkeypatch):
    import research_council.ingest as module

    mapping = workspace / "contexts/resources/angel-investment/context-map.json"
    before = mapping.read_bytes()
    atomic_write = module._atomic_bytes

    def fail_on_map(path, data):
        if path == mapping:
            raise OSError("simulated write failure")
        atomic_write(path, data)

    monkeypatch.setattr(module, "_atomic_bytes", fail_on_map)
    with pytest.raises(OSError):
        ingest(workspace)
    assert mapping.read_bytes() == before
    assert not (workspace / "contexts/resources/catalog.web.json").exists()
    assert not (workspace / "contexts/resources/angel-investment/raw/AI001").exists()
    assert not (workspace / "contexts/resources/.import.lock").exists()


def test_existing_import_lock_blocks_mutation(workspace):
    (workspace / "contexts/resources/.import.lock").touch()
    with pytest.raises(ValueError, match="import"):
        ingest(workspace)
    assert not (workspace / "contexts/resources/catalog.web.json").exists()
