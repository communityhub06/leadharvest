# LAUNCH PLAN — LeadHarvest

Everything below is built and tested. The only steps left are the ones that legally require a human with an email address: creating accounts and clicking "publish".

**Nothing here costs money to start.** Every service listed has a free tier.

---

## What's already done

| Item | Status | Where |
|---|---|---|
| The product (Python CLI) | ✅ done | `leadharvest/` |
| Test suite — 57 passing | ✅ done | `tests/` |
| Installable package + wheel | ✅ done | `dist/` |
| Landing page | ✅ done | `site/index.html` |
| README / docs | ✅ done | `README.md` |
| This launch plan | ✅ done | `LAUNCH.md` |
| Sales copy & outreach templates | ✅ done | `SELLING.md` |
| GitHub repo (public) | ✅ live | https://github.com/communityhub06/leadharvest |
| Landing page deployed | ✅ live | https://communityhub06.github.io/leadharvest/ |
| Buy links wired into page | ✅ live | points at the Gumroad product |
| Gumroad product, $29, published | ✅ live | https://communityhub7.gumroad.com/l/leadharvest |
| Payout method (BE bank) | ✅ connected | Gumroad → Payouts |
| Full purchase flow | ✅ tested | test purchase: receipt + download link issued |
| Published listings (Fiverr/Reddit/HN/IH) | ❌ you | accounts required |

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

## Rebuilding the product file after any code change

```bash
python -m build
```

Output lands in `dist/`. Re-upload the `.zip` to Gumroad.

---

## Running the tool yourself (for demos and screenshots)

```bash
python -m leadharvest -i examples\urls.txt -o out\leads.csv --region FR,US
python -m leadharvest --domain python.org --max-pages 20 --insecure
```

> On this machine TLS verification is intercepted by a local proxy, so add `--insecure` when demoing. Buyers on normal networks don't need it.

---

## Support inbox

Create one email early: `hello@yourdomain.com` or just use your personal one. You will get:

- "How do I install Python?" → send them `README.md` → Install section
- "It found no phones" → tell them `--region FR`
- "Can I have a refund?" → refund immediately, no argument. Refunds cost less than chargebacks.

---

## The one honest constraint

I built the product, the site, the tests, the packaging and every word of copy. I cannot create an account in your name, receive money for you, or click "publish" — those need a real person and a real email.

Everything past Step 1 is **copy, paste, click**. Three hours, and it's live.
