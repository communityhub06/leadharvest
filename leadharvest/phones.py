from __future__ import annotations

import re

import phonenumbers as pn

_EXT_SUFFIX = re.compile(r"(?i)\s*(?:ext\.?|extension|x)\s*\d+\s*$")
_LETTERS = re.compile(r"[A-Za-z]{3,}")
_E164 = pn.PhoneNumberFormat.E164


def clean_phone(raw: str, regions: tuple[str, ...] | None = None) -> str | None:
    """Validate a phone candidate and return it in E.164 form, or None."""
    text = raw.strip()
    if text.lower().startswith("tel:"):
        text = text[4:].strip()
    text = _EXT_SUFFIX.sub("", text).strip()
    if not text or _LETTERS.search(text):
        return None

    for region in regions or (None,):
        try:
            parsed = pn.parse(text, region)
        except pn.NumberParseException:
            continue
        if pn.is_valid_number(parsed):
            return pn.format_number(parsed, _E164)
    return None


def phones_from_text(text: str, regions: tuple[str, ...] | None = None) -> list[str]:
    """Pull valid numbers out of free text using context-aware matching."""
    found: list[str] = []
    seen: set[str] = set()
    for region in regions or (None,):
        try:
            for match in pn.PhoneNumberMatcher(text, region, max_tries=500):
                e164 = pn.format_number(match.number, _E164)
                if e164 not in seen:
                    seen.add(e164)
                    found.append(e164)
        except (pn.NumberParseException, ValueError):
            continue
    return found
