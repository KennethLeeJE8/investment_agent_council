import json

import pytest

from research_council.catalog import Catalog


def test_search_is_primary_scoped_and_has_line_citations(workspace):
    hits = Catalog(workspace).search("angel-investment", "recombination", limit=2)
    assert len(hits) == 2
    assert {hit.source_id for hit in hits} == {"BN05"}
    assert all(hit.start_line >= 1 and hit.end_line <= 45 for hit in hits)
    assert all("angel-investment exclusive" in hit.text for hit in hits)


def test_secondary_requires_explicit_opt_in(workspace):
    catalog = Catalog(workspace)
    assert [s.id for s in catalog.sources("angel-investment")] == ["BN05"]
    assert {s.id for s in catalog.sources("angel-investment", include_secondary=True)} == {
        "BN01",
        "BN05",
    }


def test_verify_detects_modified_raw(workspace):
    catalog = Catalog(workspace)
    source = catalog.sources("angel-investment")[0]
    (workspace / source.raw_path).write_text("changed")
    with pytest.raises(ValueError, match="integrity"):
        catalog.search("angel-investment", "changed")


@pytest.mark.parametrize("value", ["../outside.md", "/etc/passwd"])
def test_catalog_rejects_outside_paths(workspace, value):
    p = workspace / "contexts/resources/catalog.json"
    data = json.loads(p.read_text())
    data["records"][0]["raw_path"] = value
    p.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="inside"):
        Catalog(workspace)


def test_symlink_escape_rejected(workspace):
    catalog = Catalog(workspace)
    p = workspace / catalog.sources("angel-investment")[0].raw_path
    p.unlink()
    p.symlink_to("/etc/passwd")
    with pytest.raises(ValueError, match="inside"):
        catalog.search("angel-investment", "root")


def test_duplicate_source_ids_rejected(workspace):
    p = workspace / "contexts/resources/catalog.json"
    data = json.loads(p.read_text())
    data["records"].append(data["records"][0])
    p.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="Duplicate"):
        Catalog(workspace)


@pytest.mark.parametrize(
    "expert,query,limit",
    [
        ("unknown", "test", 2),
        ("angel-investment", "", 2),
        ("angel-investment", "test", 0),
        ("angel-investment", "test", 11),
    ],
)
def test_invalid_search_inputs_fail(workspace, expert, query, limit):
    with pytest.raises(ValueError):
        Catalog(workspace).search(expert, query, limit=limit)


def test_ascii_search_uses_whole_words(workspace):
    assert Catalog(workspace).search("angel-investment", "recomb") == []


def test_passages_include_the_exact_verified_source_hash(workspace):
    catalog = Catalog(workspace)
    source = catalog.sources("angel-investment")[0]
    hit = catalog.search("angel-investment", "recombination")[0]
    assert hit.raw_sha256 == source.sha256
    assert hit.text_sha256 == source.text_sha256
