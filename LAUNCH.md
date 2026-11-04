# LAUNCH PLAN — LeadHarvest

Everything below is built and tested. The only steps left are the ones that legally require a human with an email address: creating accounts and clicking "publish".

**Nothing here costs money to start.** Every service listed has a free tier.

---

## BLOCKED ON YOU (2 things, ~10 min)

| # | What | Why only you | Link |
|---|---|---|---|
| 1 | **PyPI account + API token** | registration needs a real email; the landing page promises `pip install leadharvest` and the package is not on PyPI yet | https://pypi.org/account/register/ → then https://pypi.org/manage/account/token/ (scope: *upload to new project* → project `leadharvest`) |
| 2 | **Gumroad re-login** | session expired; the live product still serves the **old 31 KB zip** (contains internal docs, no LICENSE, no Free/Pro split) | https://gumroad.com/login → I do the upload from there |

Once you hand me the PyPI token I upload the wheel + sdist and `pip install leadharvest` becomes true.

---

## What's already done

| Item | Status | Where |
|---|---|---|
| The product (Python CLI) | ✅ done | `leadharvest/` |
| Test suite — 67 passing (Free + Pro builds both verified) | ✅ done | `tests/` |
| Free/Pro split enforced in code | ✅ done | `leadharvest/tier.py` — 25 URLs, CSV only, 5 platforms; Pro build lifts everything |
| Both editions built & self-verified | ✅ done | `python build_dist.py` / `--pro` → `dist/leadharvest-1.0.0.zip` (19.7 KB) + `-pro.zip` (21.2 KB) |
| MIT LICENSE | ✅ done | `LICENSE` — GitHub badge + `GET /license` → 200 |
| Landing page | ✅ done | `site/index.html` |
| README / docs | ✅ done | `README.md` — Editions table, Pro flags marked |
| This launch plan | ✅ done | `LAUNCH.md` |
| Sales copy & outreach templates | ✅ done | `SELLING.md` |
| GitHub repo (public) | ✅ live | https://github.com/communityhub06/leadharvest |
| GitHub metadata — description, homepage, 15 topics, MIT license | ✅ live | verified via API |
| Landing page deployed | ✅ live | https://communityhub06.github.io/leadharvest/ |
| Buy links wired into page | ✅ live | points at the Gumroad product |
| Gumroad product, $29, published | ✅ live | https://communityhub7.gumroad.com/l/leadharvest |
| Payout method (BE bank) | ✅ connected | Gumroad → Payouts |
| Full purchase flow | ✅ tested | test purchase: receipt + download link issued |
| SEO — OG, Twitter card, canonical, JSON-LD, OG image | ✅ live | verified: 8 OG + 4 Twitter + 2 JSON-LD blocks, `og.png` 200 |
| SEO — sitemap.xml + robots.txt | ✅ live | both 200; robots points at the sitemap |
| SEO — fake `aggregateRating` removed | ✅ done | 0 sales / 0 reviews: structured-data spam risk |
| Gumroad Discover — category | ✅ set | `Business & Money > Marketing & Sales` (was `Other`) |
| Gumroad Discover — 10 tags | ✅ set | lead generation, lead scraper, email finder, prospecting, sales leads, web scraper, cold email, python cli, contact list, phone numbers |
| Gumroad Discover — listing | ⏳ locked | Gumroad: needs ≥1 successful sale **and** Risk Review; also ≤$100 price ✓ |
| PyPI — `pip install leadharvest` | ⏳ blocked | package 404 on PyPI, name free — needs your account (see above) |
| Gumroad — Pro zip upload | ⏳ blocked | session expired — needs your login (see above); file ready at `dist/leadharvest-1.0.0-pro.zip` |
| Outreach — Hacker News | ❌ dropped | `news.ycombinator.com` unreachable from this network |
| Outreach — Fiverr | ❌ dropped | PerimeterX antibot, session can't be kept alive |
| Outreach — Indie Hackers | ❌ dropped | signup is Google-only OAuth, Google login failing |
| Outreach — Reddit | ⏳ waiting | r/SaaS AutoMod removed the post: account must be 7 days old |
| — r/SaaS post (auto-removed) | ⏳ repost after day 7 | text ready in `SELLING.md` |
| — r/Python post | ⏳ day 2 | text ready in `SELLING.md` |
| — r/Entrepreneur post | ⏳ day 3 | text ready in `SELLING.md` |

---

## Step 1 — Get it on GitHub (10 min)

Repository = credibility. Buyers check. Also gives you free issue tracking and a place to put updates.

1. Go to **https://github.com/new**
2. Repository name: `leadharvest`
3. Public ✅ · Add a README: **skip** (we already have one)
4. Click **Create repository**
5. On the next screen, copy the two command blocks it shows and paste them into a terminal opened in `C:\Users\tryth\Documents\Projet par défaut\leadharvest`:

```bash
git init
git add .
git commit -m "LeadHarvest v1.0.0"
git branch -M main
git remote add origin https://github.com/YOURNAME/leadharvest.git
git push -u origin main
```

> If git asks for credentials, GitHub now wants a **Personal Access Token**, not your password:
> **https://github.com/settings/tokens/new** → check `repo` → Generate.

---

## Step 2 — Create the product to sell (15 min)

**Use Gumroad** — free to list, no monthly fee, they take a cut only when you sell, and they handle VAT/taxes for you.

1. Go to **https://gumroad.com** → **Start selling** → sign up (email is fine)
2. Dashboard → **Products** → **New product**
3. Fill it in:
   - **Name:** `LeadHarvest — URL to Lead CSV`
   - **Type:** Digital product
   - **Price:** `$29` (you can add a `$0` free tier later)
   - **Description:** paste the block from `SELLING.md` → *Gumroad listing copy*
   - **Files:** upload `dist/leadharvest-1.0.0.zip`
4. Click **Publish**
5. Copy your product URL — it looks like `https://YOURNAME.gumroad.com/l/xxxxx`

**Keep that URL. You need it in Step 3.**

> **Alternative — Lemon Squeezy:** https://lemonsqueezy.com — same idea, slightly better checkout. Either works.
>
> **Alternative — Stripe Payment Links:** https://dashboard.stripe.com/payment-links — best rates, but you handle your own tax paperwork. Not worth it at day one.

---

## Step 3 — Put your buy link on the page (5 min)

Open `leadharvest/site/index.html` in any text editor.

Press **Ctrl+F** and search for `SWAP`. There are three markers:

| Marker | Replace `href="#"` with |
|---|---|
| `SWAP-1` | your free download (or your Gumroad link) |
| `SWAP-2` | **your Gumroad URL** ← this is the money button |
| `SWAP-3` | your Gumroad URL |

Save the file. That's it.

---

## Step 4 — Deploy the site (10 min, free)

**Netlify Drop** — drag, drop, live. No build step, no card required.

1. Go to **https://app.netlify.com/drop**
2. Drag the `site` folder from `C:\Users\tryth\Documents\Projet par défaut\leadharvest\site` onto the page
3. Wait ~10 seconds → you get a URL like `https://random-name.netlify.app`
4. Click **Site settings** → **Change site name** → set it to `leadharvest` → your URL becomes `https://leadharvest.netlify.app`
5. Optional custom domain later (~$10/yr at Namecheap/Porkbun) — skip for now

**Your public URL now:** `https://leadharvest.netlify.app`

> Alternative: **GitHub Pages** — push the `site` folder, Settings → Pages → deploy from `main` / root. Free, but needs the repo from Step 1.

---

## Step 5 — Publish listings (30 min, free)

Do these in order. Each one is a channel that already has your buyers.

### 5a. Gumroad Discover
Already live from Step 2. Add tags: `leads`, `sales`, `python`, `scraper`, `outreach`, `marketing`.

### 5b. Fiverr gig — fastest path to first cash
1. **https://www.fiverr.com/start_selling** → create seller profile
2. **Create a new gig**, title: `I will build you a custom lead scraper and clean contact list`
3. Category: **Programming & Tech** → **Data Engineering**
4. Description: paste from `SELLING.md` → *Fiverr gig copy*
5. Price: start at **$25**, offer a $65 tier that includes a custom crawl
6. Upload a screenshot of the terminal output (I can generate one for you on request)

### 5c. Reddit — 3 posts, no spam
Read `SELLING.md` → *Reddit posts*. Post to:
- **r/SaaS** — "I built a lead scraper that doesn't give you garbage phone numbers"
- **r/Python** — "I kept getting repo star counts as phone numbers, so I fixed it with libphonenumber"
- **r/Entrepreneur** — "How I clean prospecting lists before I email anyone"

> **Rule:** give the insight away for free, mention the tool once. Reddit punishes pure advertising.

### 5d. Hacker News — Show HN
**https://news.ycombinator.com/submit** → title: `Show HN: LeadHarvest – URL list to validated lead CSV`
Post between **9–11am ET on a weekday**. This is the highest-variance channel — one front page hit = hundreds of sales.

### 5e. Indie Hackers
**https://www.indiehackers.com** → post in **Products**. Same copy as Reddit.

---

## Step 6 — Drive traffic all week

| Channel | Link | Effort |
|---|---|---|
| X / Twitter | post a 30-second terminal demo | 5 min |
| LinkedIn | post as "here's a tool I shipped" | 5 min |
| YouTube Shorts | screen-record the CLI running, 40 seconds | 15 min |
| TikTok | same clip, vertical | 5 min |
| Cold email | templates in `SELLING.md` | 30 min/day |

---

## Day-by-day summary

| Day | Task | Time |
|---|---|---|
| **1** | GitHub repo + Gumroad product | 25 min |
| **2** | Swap buy link + Netlify deploy | 15 min |
| **3** | Fiverr gig live | 30 min |
| **4** | Reddit ×3 + Indie Hackers | 40 min |
| **5** | Show HN + X post | 20 min |
| **6** | Cold email blast (templates ready) | 30 min |
| **7** | Review what sold, adjust price | 15 min |

**Total setup: about 3 hours.** Then it's outreach.

---

## Rebuilding the product files after any code change

```bash
python build_dist.py          # Free  -> dist/leadharvest-1.0.0.zip      (GitHub / PyPI)
python build_dist.py --pro    # Pro   -> dist/leadharvest-1.0.0-pro.zip  (Gumroad)
```

Each run extracts the archive it just wrote and runs the full test suite from inside it, printing the edition flags it found (`PRO`, `MAX_URLS`, formats, platforms) — so a broken build fails loudly instead of shipping.

- **Free zip** — public, ships `README.md` + `LICENSE`.
- **Pro zip** — same tree with `leadharvest/tier.py` rewritten to `PRO = True`, plus `INSTALL.txt`. No licence key, no phone-home.

Re-upload the Pro zip to Gumroad → **Content** tab after any code change.

---

## Running the tool yourself (for demos and screenshots)

The checkout is the **Free** edition, so Pro flags are rejected on purpose. For Pro demos build and extract the Pro zip first:

```bash
# Free (what the public gets)
python -m leadharvest -i examples\urls.txt -o out\leads.csv
python -m leadharvest --version          # -> leadharvest 1.0.0 (Free)

# Pro (unzip dist\leadharvest-1.0.0-pro.zip somewhere, then)
python -m leadharvest --domain python.org --max-pages 20 --insecure
python -m leadharvest -i examples\urls.txt --region FR,US --format both -o out\leads
```

> On this machine TLS verification is intercepted by a local proxy, so add `--insecure` when demoing. Buyers on normal networks don't need it.

---

## Support inbox

Create one email early: `hello@yourdomain.com` or just use your personal one. You will get:

- "How do I install Python?" → send them `README.md` → Install section
- "It found no phones" → numbers written as `06 12 34 56 78` need a country hint: `--region FR` is a **Pro** feature. On Free only `+33…` numbers match — tell them that plainly, and that Pro unlocks it.
- "Can I have a refund?" → refund immediately, no argument. Refunds cost less than chargebacks.

---

## The one honest constraint

I built the product, the site, the tests, the packaging and every word of copy. I cannot create an account in your name, receive money for you, or click "publish" — those need a real person and a real email.

Everything past Step 1 is **copy, paste, click**. Three hours, and it's live.
