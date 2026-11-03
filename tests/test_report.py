import csv
import json
from pathlib import Path

from leadharvest.models import Lead
from leadharvest.report import COLUMNS, to_row, write_csv, write_json


def sample_leads() -> list[Lead]:
    return [
        Lead(
            url="https://acme.fr",
            name="Acme",
            emails=["a@acme.fr", "b@acme.fr"],
            phones=["+33472000000"],
            social={"linkedin": "https://linkedin.com/acme", "twitter": "https://x.com/acme"},
            description="Builds things",
        ),
        Lead(url="https://broken.fr", error="timeout"),
    ]


def test_row_has_every_column():
    row = to_row(sample_leads()[0])
    assert set(row) == set(COLUMNS)
    assert row["emails"] == "a@acme.fr; b@acme.fr"
    assert row["linkedin"] == "https://linkedin.com/acme"


def test_write_csv_roundtrip(tmp_path: Path):
    path = write_csv(sample_leads(), tmp_path / "leads.csv")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert rows[0]["domain"] == "acme.fr"
    assert rows[1]["error"] == "timeout"


def test_write_json_roundtrip(tmp_path: Path):
    path = write_json(sample_leads(), tmp_path / "leads.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload[0]["emails"] == ["a@acme.fr", "b@acme.fr"]
    assert payload[1]["error"] == "timeout"


def test_csv_creates_parent_dirs(tmp_path: Path):
    path = write_csv(sample_leads(), tmp_path / "nested" / "out.csv")
    assert path.exists()
