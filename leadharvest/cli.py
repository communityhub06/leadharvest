from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from . import __version__, tier
from .crawl import crawl
from .extract import extract
from .fetch import canonical_url, fetch, make_session
from .models import Lead
from .normalize import normalize_lead
from .report import write_csv, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="leadharvest",
        description="Harvest emails, phones and social profiles from any list of URLs.",
    )
    parser.add_argument("targets", nargs="*", help="URLs to harvest")
    parser.add_argument("-i", "--input", help="file with one URL per line (# comments allowed)")
    parser.add_argument("-d", "--domain", help="seed domain to crawl for URLs")
    parser.add_argument("--max-pages", type=int, default=25, help="crawl page budget (default 25)")
    parser.add_argument("--depth", type=int, default=2, help="crawl link depth (default 2)")
    parser.add_argument("-o", "--output", default="leads.csv", help="output path (default leads.csv)")
    parser.add_argument("--format", choices=("csv", "json", "both"), default="csv")
    parser.add_argument("-j", "--jobs", type=int, default=8, help="parallel requests (default 8)")
    parser.add_argument("--timeout", type=float, default=15.0, help="per-request seconds (default 15)")
    parser.add_argument(
        "--region",
        help="default region(s) for national phone numbers, comma-separated ISO codes (e.g. FR,US)",
    )
    parser.add_argument("--insecure", action="store_true", help="skip TLS verification")
    parser.add_argument("--quiet", action="store_true", help="suppress progress output")
    parser.add_argument(
        "--version",
        action="version",
        version=f"leadharvest {__version__} ({tier.edition()})",
    )
    return parser


def enforce_tier(args: argparse.Namespace) -> None:
    """Reject Pro features before any network I/O happens."""
    if args.format not in tier.FORMATS:
        raise SystemExit(tier.blocked(f"--format {args.format}", "JSON and dual export are included"))
    if args.domain and not tier.CRAWL:
        raise SystemExit(tier.blocked("--domain", "crawl mode is included"))
    if args.region and not tier.REGIONS:
        raise SystemExit(tier.blocked("--region", "multi-region phone parsing is included"))


def parse_regions(value: str | None) -> tuple[str, ...] | None:
    if not value:
        return None
    regions = tuple(part.strip().upper() for part in value.split(",") if part.strip())
    for code in regions:
        if len(code) != 2 or not code.isalpha():
            raise SystemExit(f"invalid region {code!r} — expected a 2-letter ISO code like FR or US")
    return regions or None


def collect_urls(args: argparse.Namespace, session) -> list[str]:
    raw: list[str] = list(args.targets)

    if args.input:
        path = Path(args.input)
        if not path.exists():
            raise SystemExit(f"input file not found: {path}")
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                raw.append(stripped)

    if args.domain:
        raw.extend(crawl(session, args.domain, args.max_pages, args.depth, args.timeout))

    ordered: list[str] = []
    seen: set[str] = set()
    for item in raw:
        url = canonical_url(item)
        if url and url not in seen:
            seen.add(url)
            ordered.append(url)
    return ordered


def harvest(
    urls: list[str],
    session,
    jobs: int,
    timeout: float,
    regions: tuple[str, ...] | None = None,
) -> list[Lead]:
    leads: list[Lead] = []
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        pending = {pool.submit(fetch, session, url, timeout): url for url in urls}
        for future in as_completed(pending):
            source = pending[future]
            final_url, html, error = future.result()
            lead = Lead(url=final_url or source)
            if error:
                lead.error = error
            else:
                extracted = extract(html, lead.url, regions)
                lead.name = extracted.name
                lead.description = extracted.description
                lead.emails = extracted.emails
                lead.phones = extracted.phones
                lead.social = extracted.social
            leads.append(normalize_lead(lead, regions))
    leads.sort(key=lambda item: (item.domain, item.url))
    return leads


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    enforce_tier(args)
    session = make_session(insecure=args.insecure)
    regions = parse_regions(args.region)

    urls = collect_urls(args, session)
    if not urls:
        print("no URLs — pass targets, --input FILE, or --domain SEED", file=sys.stderr)
        return 2

    if tier.MAX_URLS is not None and len(urls) > tier.MAX_URLS:
        raise SystemExit(
            f"{len(urls)} URLs found — the Free edition runs {tier.MAX_URLS} at a time.\n"
            f"Split the list into batches, or unlock unlimited: {tier.UPGRADE_URL}"
        )

    if not args.quiet:
        print(f"harvesting {len(urls)} URL(s)...", file=sys.stderr)

    leads = harvest(urls, session, args.jobs, args.timeout, regions)

    stem = Path(args.output)
    written: list[Path] = []
    if args.format in ("csv", "both"):
        written.append(write_csv(leads, stem if stem.suffix else stem.with_suffix(".csv")))
    if args.format in ("json", "both"):
        base = stem.with_suffix("") if stem.suffix else stem
        written.append(write_json(leads, base.with_suffix(".json")))

    hits = [lead for lead in leads if lead.emails]
    emails = sum(len(lead.emails) for lead in leads)
    phones = sum(len(lead.phones) for lead in leads)
    failed = sum(1 for lead in leads if lead.error)

    if not args.quiet:
        print(
            f"done — {len(leads)} sites | {len(hits)} with email | "
            f"{emails} emails | {phones} phones | {failed} failed",
            file=sys.stderr,
        )
        for path in written:
            print(f"wrote {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
