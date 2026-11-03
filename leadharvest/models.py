from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass
class Lead:
    url: str
    domain: str = ""
    name: str = ""
    description: str = ""
    emails: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    social: dict[str, str] = field(default_factory=dict)
    error: str = ""

    def __post_init__(self) -> None:
        if not self.domain:
            self.domain = host_of(self.url)


def host_of(url: str) -> str:
    host = urlparse(url if "://" in url else f"https://{url}").netloc.lower()
    return host[4:] if host.startswith("www.") else host
