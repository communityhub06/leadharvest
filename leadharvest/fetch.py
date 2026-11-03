from __future__ import annotations

import random
from urllib.parse import urlparse

import requests
from requests import Session

USER_AGENTS = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
)

MAX_BYTES = 5_000_000


def make_session(insecure: bool = False) -> Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        }
    )
    session.trust_env = False
    if insecure:
        session.verify = False
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return session


def canonical_url(raw: str) -> str | None:
    value = raw.strip()
    if not value or value.startswith("#"):
        return None
    if "://" not in value:
        value = f"https://{value}"
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None
    return parsed._replace(fragment="").geturl()


def fetch(session: Session, url: str, timeout: float = 15.0) -> tuple[str, str, str]:
    """Return (final_url, html, error). Exactly one of html/error is populated."""
    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
    except Exception as exc:
        return url, "", f"{type(exc).__name__}: {exc}"

    ctype = (response.headers.get("content-type") or "").lower()
    if ctype and not any(kind in ctype for kind in ("html", "xml", "text/plain")):
        return response.url, "", f"skipped content-type {ctype.split(';')[0]}"

    payload = response.content[:MAX_BYTES]
    encoding = _charset(response) or "utf-8"
    try:
        html = payload.decode(encoding, errors="replace")
    except LookupError:
        html = payload.decode("utf-8", errors="replace")
    return response.url, html, ""


def _charset(response) -> str | None:
    """Prefer an explicit charset; otherwise sniff, since requests defaults to latin-1."""
    content_type = (response.headers.get("content-type") or "").lower()
    if "charset" in content_type:
        for param in content_type.split(";"):
            if "charset" in param and "=" in param:
                return param.split("=", 1)[-1].strip().strip("\"'")
    try:
        return response.apparent_encoding
    except Exception:
        return None
