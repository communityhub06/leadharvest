from __future__ import annotations

from .extract import FILE_TLDS
from .models import Lead
from .phones import clean_phone

_TRAILING = ".,;:)>]}\"'|"


def clean_email(raw: str) -> str | None:
    email = raw.strip().strip(_TRAILING).lower()
    if email.count("@") != 1 or len(email) > 254:
        return None

    local, _, domain = email.partition("@")
    if not local or len(local) > 64 or "." not in domain:
        return None
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return None
    if any(ch in local for ch in " <>\"'\\,"):
        return None

    tld = domain.rsplit(".", 1)[-1]
    if not tld.isalpha() or not 2 <= len(tld) <= 24 or tld in FILE_TLDS:
        return None
    if any(part == "" or part.startswith("-") or part.endswith("-") for part in domain.split(".")):
        return None
    return email


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def normalize_lead(lead: Lead, regions: tuple[str, ...] | None = None) -> Lead:
    lead.emails = sorted(unique(filter(None, (clean_email(e) for e in lead.emails))))
    lead.phones = sorted(unique(filter(None, (clean_phone(p, regions) for p in lead.phones))))
    lead.social = dict(sorted(lead.social.items()))
    lead.name = lead.name.strip()
    lead.description = lead.description.strip()
    return lead
