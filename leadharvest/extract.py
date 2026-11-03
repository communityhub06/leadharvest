from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .phones import clean_phone, phones_from_text

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,24}")

FILE_TLDS = frozenset(
    (
        "png jpg jpeg gif svg webp ico bmp css js mjs json xml html htm php asp aspx "
        "txt md log woff woff2 ttf otf eot mp4 mp3 wav ogg webm pdf zip rar tar gz "
        "doc docx xls xlsx ppt pptx exe dll so dylib bin dat db sqlite map"
    ).split()
)

SOCIAL_RULES: tuple[tuple[str, str], ...] = (
    ("linkedin.com", "linkedin"),
    ("twitter.com", "twitter"),
    ("x.com", "twitter"),
    ("facebook.com", "facebook"),
    ("instagram.com", "instagram"),
    ("youtube.com", "youtube"),
    ("youtu.be", "youtube"),
    ("tiktok.com", "tiktok"),
    ("github.com", "github"),
    ("pinterest.com", "pinterest"),
    ("medium.com", "medium"),
    ("reddit.com", "reddit"),
    ("threads.net", "threads"),
    ("snapchat.com", "snapchat"),
    ("t.me", "telegram"),
    ("discord.gg", "discord"),
)

_DROP_TAGS = ("script", "style", "noscript", "svg", "template", "iframe")


@dataclass
class Extracted:
    name: str = ""
    description: str = ""
    emails: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    social: dict[str, str] = field(default_factory=dict)


def _squash(value: str, limit: int = 300) -> str:
    return re.sub(r"\s+", " ", value).strip()[:limit]


def social_platform(url: str) -> str | None:
    host = urlparse(url if "://" in url else f"https://{url}").netloc.lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    for suffix, platform in SOCIAL_RULES:
        if host == suffix or host.endswith("." + suffix):
            return platform
    return None


def _meta_content(soup: BeautifulSoup, value: str, attr: str) -> str:
    for tag in soup.find_all("meta"):
        if (tag.get(attr) or "").strip().lower() == value:
            content = tag.get("content")
            if content and content.strip():
                return _squash(content)
    return ""


def _site_name(soup: BeautifulSoup) -> str:
    for key, attr in (("og:site_name", "property"), ("application-name", "name"), ("twitter:site", "name")):
        found = _meta_content(soup, key, attr)
        if found:
            return found.lstrip("@")
    if soup.title:
        return _squash(soup.title.get_text())
    h1 = soup.find("h1")
    return _squash(h1.get_text(" ")) if h1 else ""


def _visible_text(soup: BeautifulSoup) -> str:
    for tag in soup.find_all(list(_DROP_TAGS)):
        tag.decompose()
    return _squash(soup.get_text(" "), limit=500_000)


def _emails_from_links(soup: BeautifulSoup) -> list[str]:
    found: list[str] = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href.lower().startswith("mailto:"):
            continue
        payload = href[7:].split("?", 1)[0]
        found.extend(re.split(r"[;,]", payload))
    return found


def _phones_from_links(soup: BeautifulSoup, regions: tuple[str, ...] | None) -> list[str]:
    found: list[str] = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if href.lower().startswith("tel:"):
            cleaned = clean_phone(href, regions)
            if cleaned:
                found.append(cleaned)
    return found


def _social_from_links(soup: BeautifulSoup, base_url: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        absolute = urljoin(base_url, href)
        platform = social_platform(absolute)
        if platform and platform not in found:
            found[platform] = absolute.split("#", 1)[0]
    return found


def extract(html: str, base_url: str = "", regions: tuple[str, ...] | None = None) -> Extracted:
    soup = BeautifulSoup(html, "html.parser")
    text = _visible_text(soup)

    return Extracted(
        name=_site_name(soup),
        description=_meta_content(soup, "description", "name")
        or _meta_content(soup, "og:description", "property"),
        emails=_emails_from_links(soup) + EMAIL_RE.findall(text),
        phones=_phones_from_links(soup, regions) + phones_from_text(text, regions),
        social=_social_from_links(soup, base_url),
    )
