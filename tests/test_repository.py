"""Exercise the CLI with a temporary workspace created by the tests."""

import json

from research_council.catalog import EXPERTS
from research_council.cli import main


def test_cli_prepares_isolated_packets_from_temporary_workspace(workspace, capsys):
    root_args = ["--root", str(workspace)]
    assert main([*root_args, "doctor"]) == 0
    assert json.loads(capsys.readouterr().out)["sources"] == len(EXPERTS)

    assert main([*root_args, "prepare", "--topic", "recombination"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "prepared_not_researched"
    folder = next((workspace / "runs").iterdir())
    assert result["output"] == str(folder)
    manifest = json.loads((folder / "manifest.json").read_text())
    assert set(manifest["experts"]) == set(EXPERTS)
    assert manifest["model_calls"] == 0
    for index, expert in enumerate(EXPERTS, start=1):
        passages = manifest["experts"][expert]["passages"]
        assert passages
        assert {p["source_id"] for p in passages} == {f"BN{index:02}"}
