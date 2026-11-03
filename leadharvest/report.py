from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import Lead

COLUMNS = (
    "domain",
    "name",
    "emails",
    "phones",
    "linkedin",
    "twitter",
    "facebook",
    "instagram",
    "youtube",
    "tiktok",
    "github",
    "website",
    "description",
    "error",
)


def _join(values: list[str]) -> str:
    return "; ".join(values)


def to_row(lead: Lead) -> dict[str, str]:
    return {
        "domain": lead.domain,
        "name": lead.name,
        "emails": _join(lead.emails),
        "phones": _join(lead.phones),
        "linkedin": lead.social.get("linkedin", ""),
        "twitter": lead.social.get("twitter", ""),
        "facebook": lead.social.get("facebook", ""),
        "instagram": lead.social.get("instagram", ""),
        "youtube": lead.social.get("youtube", ""),
        "tiktok": lead.social.get("tiktok", ""),
        "github": lead.social.get("github", ""),
        "website": lead.url,
        "description": lead.description,
        "error": lead.error,
    }


def write_csv(leads: list[Lead], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for lead in leads:
            writer.writerow(to_row(lead))
    return target


def write_json(leads: list[Lead], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "domain": lead.domain,
            "name": lead.name,
            "url": lead.url,
            "emails": lead.emails,
            "phones": lead.phones,
            "social": lead.social,
            "description": lead.description,
            "error": lead.error,
        }
        for lead in leads
    ]
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return target
