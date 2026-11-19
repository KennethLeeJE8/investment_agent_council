import json
import socket

import pytest

from research_council.cli import main
from research_council.workflow import prepare


def test_prepare_writes_isolated_real_context_not_simulated_findings(workspace):
    folder = prepare(workspace, "recombination", context_chars=12000)
    manifest = json.loads((folder / "manifest.json").read_text())
    assert manifest["status"] == "prepared_not_researched"
    assert manifest["model_calls"] == 0 and not manifest["remote_ingestion"]
    packs = list((folder / "contexts").glob("*.md"))
    assert len(packs) == 6
    for p in packs:
        text = p.read_text()
        assert f"# {p.stem}\nOnly my charter." in text
        assert len(text) <= 12000
        assert "No independent research or investment conclusions" in text
        for other in packs:
            if other != p:
                assert f"# {other.stem}\nOnly my charter." not in text
                assert f"{other.stem} exclusive evidence" not in text
    spans = [json.loads(x) for x in (folder / "traces.jsonl").read_text().splitlines()]
    assert any(s["name"] == "council.prepare" for s in spans)
    assert all("recombination" not in json.dumps(s.get("attributes", {})) for s in spans)
    assert (folder / "brief.md").exists()


def test_small_budget_fails_before_output(workspace):
    with pytest.raises(ValueError, match="budget"):
        prepare(workspace, "test", context_chars=20)
    assert not list((workspace / "runs").glob("*/manifest.json"))


@pytest.mark.parametrize("topic", ["", "   ", "x" * 4001])
def test_invalid_topic_rejected(workspace, topic):
    with pytest.raises(ValueError, match="topic"):
        prepare(workspace, topic)


def test_cli_doctor_never_prints_keys(workspace, capsys, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-test-value")
    assert main(["--root", str(workspace), "doctor"]) == 0
    out = capsys.readouterr().out
    assert "secret-test-value" not in out
    assert json.loads(out)["sources"] == 6


def test_cli_sources_and_live_failure(workspace, capsys):
    assert (
        main(
            [
                "--root",
                str(workspace),
                "sources",
                "search",
                "--expert",
                "angel-investment",
                "--query",
                "recombination",
            ]
        )
        == 0
    )
    assert "BN05" in capsys.readouterr().out
    assert main(["--root", str(workspace), "run", "--topic", "example"]) == 2
    assert "not implemented" in capsys.readouterr().err


def test_prepare_stays_offline_with_inherited_tracing_settings(workspace, monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "true")
    monkeypatch.setenv("LANGSMITH_API_KEY", "unused-test-secret")

    def reject_network(*args, **kwargs):
        pytest.fail("Preparation attempted a network connection")

    monkeypatch.setattr(socket.socket, "connect", reject_network)
    folder = prepare(workspace, "recombination")
    assert (folder / "manifest.json").exists()


def test_failed_write_is_not_reported_as_complete(workspace, monkeypatch):
    import research_council.workflow as workflow

    def fail(*args):
        raise OSError("simulated disk failure")

    monkeypatch.setattr(workflow, "_write_bundle", fail)
    with pytest.raises(OSError):
        prepare(workspace, "recombination")
    assert len(list((workspace / "runs").glob("*/FAILED.txt"))) == 1
    assert not list((workspace / "runs").glob("*/manifest.json"))


def test_chinese_query_finds_and_cites_source(workspace):
    import hashlib

    from research_council.catalog import Catalog

    path = workspace / "contexts/resources/angel-investment/raw/BN05.md"
    path.write_text("创始人的适应能力需要观察。\n")
    catalog_path = workspace / "contexts/resources/catalog.json"
    data = json.loads(catalog_path.read_text())
    data["records"][4]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    catalog_path.write_text(json.dumps(data))
    hits = Catalog(workspace).search("angel-investment", "适应能力")
    assert hits[0].source_id == "BN05"
    assert hits[0].start_line == hits[0].end_line == 1
