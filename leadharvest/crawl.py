from __future__ import annotations

from collections import deque
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from requests import Session

from .fetch import canonical_url, fetch


def _host(url: str) -> str:
    host = urlparse(url).netloc.lower().split(":")[0]
    return host[4:] if host.startswith("www.") else host


def _same_site(a: str, b: str) -> bool:
    left, right = _host(a), _host(b)
    return left == right or left.endswith("." + right) or right.endswith("." + left)


def _links(html: str, base: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    found: list[str] = []
    for anchor in soup.find_all("a", href=True):
        absolute = canonical_url(urljoin(base, anchor["href"]))
        if absolute and absolute.startswith(("http://", "https://")):
            found.append(absolute)
    return found


def crawl(
    session: Session,
    seed: str,
    max_pages: int = 25,
    depth: int = 2,
    timeout: float = 15.0,
) -> list[str]:
    start = canonical_url(seed)
    if not start:
        return []

    visited: set[str] = set()
    queued: set[str] = {start}
    queue: deque[tuple[str, int]] = deque([(start, 0)])
    harvested: list[str] = []

    while queue and len(harvested) < max_pages:
        url, level = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        harvested.append(url)

        if level >= depth:
            continue

        final_url, html, error = fetch(session, url, timeout)
        if error:
            continue
        for link in _links(html, final_url):
            if link in queued or link in visited:
                continue
            if not _same_site(link, start):
                continue
            queued.add(link)
            queue.append((link, level + 1))

    return harvested[:max_pages]
