import hashlib
import json

import pytest

EXPERTS = (
    "technology-evolution",
    "sexual-selection",
    "natural-selection",
    "cultural-evolution",
    "angel-investment",
    "venture-capital",
)


@pytest.fixture
def workspace(tmp_path):
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "test-council"\n')
    contexts = tmp_path / "contexts"
    (contexts / "experts").mkdir(parents=True)
    (contexts / "SHARED_RESEARCH_RULES.md").write_text("Attribute sources. Keep experts separate.")
    records = []
    for i, expert in enumerate(EXPERTS):
        (contexts / "experts" / f"{expert}.md").write_text(f"# {expert}\nOnly my charter.")
        folder = contexts / "resources" / expert
        (folder / "raw").mkdir(parents=True)
        source_id = f"BN{i + 1:02}"
        text = f"{expert} exclusive evidence about recombination.\n" * 45
        path = folder / "raw" / f"{source_id}.md"
        path.write_text(text)
        records.append(
            {
                "id": source_id,
                "owner": expert,
                "title": f"{expert} source",
                "raw_path": str(path.relative_to(tmp_path)),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "secondary": ["angel-investment"] if i == 0 else [],
            }
        )
        (folder / "context-map.json").write_text(
            json.dumps(
                {
                    "primary_note_ids": [source_id],
                    "secondary_note_ids": ["BN01"] if expert == "angel-investment" else [],
                }
            )
        )
    (contexts / "resources" / "catalog.json").write_text(json.dumps({"records": records}))
    return tmp_path
