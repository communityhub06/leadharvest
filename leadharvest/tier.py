"""Edition limits for this build.

The public build — GitHub and PyPI — is Free: 25 URLs per run, CSV only, no
crawl, no region hints, five social platforms. The build shipped on Gumroad
sets ``PRO = True`` and lifts every limit.

There is no licence key, no activation server and no telemetry. The limit is
whatever this file says, and this file ships inside the code you are running.
"""

from __future__ import annotations

PRO = False

UPGRADE_URL = "https://communityhub7.gumroad.com/l/leadharvest"

MAX_URLS: int | None = None if PRO else 25
FORMATS: tuple[str, ...] = ("csv", "json", "both") if PRO else ("csv",)
CRAWL: bool = PRO
REGIONS: bool = PRO

#: Platforms the Free edition resolves. Pro resolves every rule in
#: :data:`leadharvest.extract.SOCIAL_RULES`.
SOCIAL: frozenset[str] | None = (
    None
    if PRO
    else frozenset(("linkedin", "twitter", "facebook", "instagram", "github"))
)

_EDITION = "Pro" if PRO else "Free"
_SUMMARY = (
    "every feature unlocked"
    if PRO
    else f"{MAX_URLS} URLs per run, CSV only, {len(SOCIAL or ())} social platforms"
)


def edition() -> str:
    """Human-readable edition name for ``--version`` and error output."""
    return _EDITION


def blocked(feature: str, why: str) -> str:
    """Message shown when a Pro feature is requested on a Free build."""
    return "\n".join(
        (
            f"{feature} is a Pro feature — {why}.",
            f"Running {_EDITION}: {_SUMMARY}.",
            f"Upgrade once, run forever: {UPGRADE_URL}",
        )
    )
