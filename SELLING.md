# SELLING.md — copy-paste assets

Everything here is ready to paste. Replace `YOURNAME` and your links.

---

## Gumroad listing copy

**Name:** LeadHarvest — URL to Lead CSV

**Tagline:** Turn any list of URLs into a clean, validated lead CSV — emails, phone numbers and social profiles in one command.

**Description:**

> ### Stop importing garbage into your outreach tool
>
> You paste 400 URLs into a scraper, get a CSV back, and spend an hour deleting numbers that aren't numbers — repository star counts, publish dates, fibonacci sequences, issue IDs.
>
> LeadHarvest validates every phone number through Google's **libphonenumber** using context-aware matching, so those never reach your list.
>
> **What it pulls:**
> - ✅ Emails — body text + `mailto:`, junk filtered (`hero@2x.png`, script contents, malformed addresses)
> - ✅ Phone numbers — validated and normalised to **E.164** (`+33472000000`), importable into any dialler
> - ✅ Social profiles — LinkedIn, X, Facebook, Instagram, YouTube, TikTok, GitHub, Telegram + more
> - ✅ Company name + meta description for your first line of outreach
>
> **What makes it different:**
> - `112 33 11` (repo stars) → rejected
> - `2026-11-03` (a date) → rejected
> - `377 610 987` (fibonacci) → rejected
> - `+33 4 72 00 00 00` → kept, delivered as `+33472000000`
>
> **How it works:**
> ```bash
> pip install leadharvest
> leadharvest -i urls.txt -o leads.csv --region FR,US
> ```
>
> **Details:**
> - Python 3.10+ · Windows / macOS / Linux
> - Runs entirely on your machine — no server, no account, no API key, no telemetry
> - CSV with UTF-8 BOM (Excel opens accents correctly) or JSON
> - Parallel fetching, crawl mode, 57 passing tests
>
> **What you get:** instant download, source included, lifetime updates.

**Tags:** `leads` `sales` `python` `scraper` `outreach` `prospecting` `marketing` `automation`

---

## Fiverr gig copy

**Gig title:** I will build you a custom lead scraper and clean contact list

**Description:**

> ### Need a clean prospecting list, not a raw scrape?
>
> I'll run your target URLs through **LeadHarvest**, a tool I built specifically to solve the junk-data problem — validated phone numbers (E.164), filtered emails, and resolved social profiles.
>
> **What you get:**
> - CSV with company name, emails, phones, LinkedIn, X, Instagram, YouTube and more
> - Phone numbers validated through Google's libphonenumber — no star counts, no dates, no garbage
> - Emails filtered for junk (image paths, script contents, malformed addresses)
> - Sorted, deduplicated, ready to import into HubSpot / Apollo / Instantly / your sequencer
>
> **Basic ($25):** up to 200 URLs → clean CSV, 24h delivery
> **Standard ($65):** up to 1,000 URLs + crawl mode to discover pages, 48h
> **Premium ($150):** up to 5,000 URLs + custom fields + a short written summary of what I found
>
> **I need from you:**
> 1. A list of URLs (or a domain and I'll crawl it)
> 2. Your target country/region (so phone numbers validate correctly)
>
> Everything is public-data only. I don't touch private databases or gated content.

**Search tags:** `lead generation` `web scraping` `data entry` `prospecting` `csv`

---

## Reddit posts

### r/SaaS
**Title:** I built a lead scraper because every other one hands you garbage phone numbers

> Every scraper I tried gave me "phone numbers" that were actually repo star counts, publish dates, and one memorable fibonacci sequence (`377 610 987`).
>
> The fix was boring but effective: run every candidate through Google's libphonenumber with context-aware matching instead of regexing for digit patterns.
>
> Before:
> `112 33 11` · `2026-11-03` · `505 160 26 10` · `377 610 987`
>
> After:
> `+33472000000` · `+33612345678`
>
> The other half was email filtering — `hero@2x.png` and `style@1.css` were passing as emails because the regex only checked for an `@` and a dot.
>
> It's open source and free to try: [link]. Curious what others use to clean lists before outreach.

### r/Python
**Title:** A regex for phone numbers will lie to you — here's what I used instead

> Spent the weekend on a deceptively simple problem: extract phone numbers from web pages.
>
> Regex approach (`\+?\d[\d\s.()/-]{7,}\d`) produced a CSV full of noise — GitHub repository stars, changelog dates, commit activity counts.
>
> What worked:
> 1. **`phonenumbers.PhoneNumberMatcher`** on the visible text — it's context-aware and skips numbers embedded in longer digit runs
> 2. **`is_valid_number()`** as a hard gate before anything hits the output
> 3. **E.164 normalisation** so the output imports cleanly into any dialler
> 4. A `--region` flag, because `06 12 34 56 78` is meaningless without a country hint
>
> Side effect worth knowing: `requests` defaults to ISO-8859-1 for `text/html` when no charset is declared, which silently mangles `™` and `—` in titles. Check `response.apparent_encoding`.
>
> Repo: [link] — 57 tests, MIT.

### r/Entrepreneur
**Title:** The unglamorous 30 minutes that determines whether your cold email works

> Nobody talks about list cleaning, but it's the difference between a campaign that lands and one that gets marked as spam.
>
> My rules before anything goes out:
> 1. **Every phone number validates** — through libphonenumber, not a regex. Invalid numbers mean your dialler burns through a list that was never real.
> 2. **No role accounts** — `info@`, `sales@` are fine, `admin@` and `hostmaster@` are not.
> 3. **Dedupe on domain, not just email** — three contacts at one company is a pile-on, not a campaign.
> 4. **Everything in E.164** — `+33472000000`, never `04 72 00 00 00`. Your sequencer will silently fail on the second one.
>
> I built this into a small tool (link) because I was doing it by hand every week.

---

## Show HN

**Title:** `Show HN: LeadHarvest – turn a URL list into a validated lead CSV`

**First comment (post this yourself, immediately after submitting):**

> I kept getting repo star counts and publish dates in my "phone number" column, so I replaced the regex with Google's libphonenumber.
>
> The interesting bit is `PhoneNumberMatcher` — it's context-aware, so `112 33 11` sitting next to a star icon is skipped, while `+33 4 72 00 00 00` three words later is picked up. A plain regex can't tell the difference.
>
> Second bug worth mentioning: `requests` sets encoding to ISO-8859-1 for `text/html` when the server omits a charset header. That silently turned `™` into a replacement character in extracted titles. Now I read an explicit charset first and fall back to `apparent_encoding`.
>
> It also pulls emails (junk-filtered) and social profiles, exports CSV/JSON, and has a crawl mode. MIT, 57 tests.
>
> Curious what others use for list cleaning — is everyone regexing and then fixing it up in Excel?

**Submit at:** https://news.ycombinator.com/submit — **9–11am ET, Tuesday–Thursday**

---

## Cold email template

**Subject:** quick one about your contact list

> Hi {{first_name}},
>
> Noticed {{company}} is doing {{specific thing you saw on their site}}.
>
> I build tools for cleaning prospecting lists — mostly because every scraper I tried handed me phone numbers that were actually repo star counts.
>
> Not pitching you anything. If you ever need a URL list turned into a validated contact CSV (emails, E.164 phones, socials), it's a one-command job and I'll do the first 200 URLs free.
>
> Either way, good luck with {{specific thing}}.
>
> {{your name}}

**Send 20/day maximum.** Warm the domain first — new domains blasting200/day get burned in a week.

---

## X / Twitter post

> i built a lead scraper that doesn't give you garbage
>
> most tools return "phone numbers" that are actually repo stars and publish dates
>
> mine validates every number through libphonenumber
>
> before: 112 33 11 · 2026-11-03 · 377 610 987
> after: +33472000000 · +33612345678
>
> [link]

---

## Pricing rationale

| Tier | Price | Why |
|---|---|---|
| Free | $0 | Removes the "does it work?" objection. 25-URL cap makes the limit felt. |
| **Pro** | **$29** | Impulse range. Below the threshold where someone asks their boss. This is your main seller. |
| Team | $79 | Anchors Pro as cheap. Almost nobody buys it early — it exists to make $29 look small. |

**Do not start cheaper.** A $9 tool reads as a toy. If you get zero sales after 100 visits, drop Pro to $19 — but never below.

**Refund policy:** instant, no questions. A refund costs you $29; a chargeback costs you $20 plus a flag on your account.
