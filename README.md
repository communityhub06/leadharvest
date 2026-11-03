# LeadHarvest

Turn any list of URLs into a clean, validated lead CSV — emails, phone numbers and social profiles in one pass.

```bash
leadharvest -i urls.txt -o leads.csv
```

```
done — 4 sites | 1 with email | 1 emails | 0 phones | 0 failed
wrote leads.csv
```

## Why it beats a regex scraper

Naive scrapers fill your CSV with star counts, dates and fibonacci sequences pretending to be phone numbers. LeadHarvest validates every number through Google's **libphonenumber**, using context-aware matching, so `112 33 11` (repo stars) and `2026-11-03` (a date) never reach your outreach list.

- **Emails** — `mailto:` links plus body text, junk filtered (`hero@2x.png`, `style@1.css`, script contents)
- **Phones** — validated and normalised to **E.164** (`+33472000000`), ready for any dialler or sequencer
- **Socials** — LinkedIn, X, Facebook, Instagram and GitHub (Pro adds YouTube, TikTok, Telegram, Discord and 7 more), absolutised
- **Names** — `og:site_name` → `<title>` → `<h1>`, plus meta description
- **Parallel** — 8 concurrent requests by default, with retries and a 5 MB page cap

## Install

```bash
pip install leadharvest
```

Requires Python 3.10+. Dependencies: `requests`, `beautifulsoup4`, `phonenumbers`.

## Editions

This build is **Free**: 25 URLs per run, CSV export, five social platforms. It
runs entirely on your machine — no account, no licence key, no telemetry.

| | Free | Pro ($29, one-time) |
|---|---|---|
| URLs per run | 25 | unlimited |
| Export | CSV | CSV + JSON |
| Crawl mode (`--domain`) | — | yes |
| Region hints (`--region`) | — | yes |
| Social platforms | 5 | 14+ |
| Support | community | priority |

Pro unlocks the features below and ships as a single zip from
<https://communityhub7.gumroad.com/l/leadharvest>. The limits live in
`leadharvest/tier.py` — that is the whole mechanism, there is nothing to phone
home to.

## Usage

```bash
# a file of URLs, one per line (# comments allowed)
leadharvest -i urls.txt -o leads.csv

# explicit targets
leadharvest https://acme.fr https://shop.example.com
```

Pro:

```bash
# crawl a whole site to discover URLs first
leadharvest --domain acme.fr --max-pages 50 --depth 3

# both CSV and JSON
leadharvest -i urls.txt --format both -o out/leads

# national numbers need a region — otherwise only +international ones match
leadharvest -i urls.txt --region FR,US
```

### Options

| Flag | Edition | Default | Purpose |
|---|---|---|---|
| `-i, --input` | Free | — | file with one URL per line |
| `-d, --domain` | Pro | — | seed domain to crawl |
| `--max-pages` | Pro | `25` | crawl page budget |
| `--depth` | Pro | `2` | crawl link depth |
| `-o, --output` | Free | `leads.csv` | output path |
| `--format` | CSV free, JSON Pro | `csv` | `csv`, `json` or `both` |
| `-j, --jobs` | Free | `8` | parallel requests |
| `--timeout` | Free | `15` | per-request seconds |
| `--region` | Pro | — | default region(s) for national phone numbers |
| `--insecure` | Free | off | skip TLS verification (corporate proxies) |
| `--quiet` | Free | off | suppress progress output |

## Output

CSV columns:

```
domain, name, emails, phones, linkedin, twitter, facebook,
instagram, youtube, tiktok, github, website, description, error
```

Multiple values are separated by `; `. The file is written UTF-8 **with BOM** so Excel opens accents correctly. Rows are sorted by domain. Unreachable sites are kept with the reason in `error` — you never silently lose a row.

```csv
acme.fr,Acme Studio,a@acme.fr; b@acme.fr,+33472000000,https://linkedin.com/company/acme,,,,,,,https://acme.fr,Fast websites for small businesses,
```

## Testing

```bash
pip install -e ".[dev]"
pytest
```

67 tests covering extraction, phone validation, email filtering, CSV/JSON round-trips, CLI parsing and the Free/Pro tier boundaries.

## Legal note

Only harvest contact details that are publicly published, and honour `robots.txt`, opt-outs and applicable anti-spam law (CAN-SPAM, GDPR, CASL) when you message anyone. This tool reads public web pages — what you do with the list is on you.

## License

MIT
