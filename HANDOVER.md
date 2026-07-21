# Hailiya Group Website — Project Handover

**Handover Date:** July 2026  
**Outgoing Developer:** Vedant  
**Project:** Hailiya Group Australia — Corporate Website  
**Live URL:** Hosted on cPanel (websitehostserver)  
**Admin Panel (Sanity CMS):** https://hailiya-group.sanity.studio *(pending setup — see below)*

---

## What This Project Is

A static HTML website for Hailiya Group Australia, the Australian distributor for Qingdao Huakai Ocean Science & Technology. The site showcases rope products across four categories (Marine, Defence, Safety, Outdoor) and displays company news.

---

## Folder Structure

```
netlify_deploy/          ← The live website. Upload contents of this folder to cPanel.
  index.html             ← Main single-page website (all sections, JS, CSS inline)
  news-article.html      ← Individual news article page
  privacy.html           ← Privacy policy page
  images/                ← All website images
    products/            ← Product card images (matched to PDFs)
    news_index*.jpg      ← News article thumbnails (scraped from hailiya.com.au)
    ...
  robots.txt
  sitemap.xml

import-products.js       ← One-time script to import products into Sanity CMS
import-news.js           ← One-time script to import news articles into Sanity CMS
package.json             ← Node.js dependencies (@sanity/client)
scrape_build_news.py     ← Python script that originally scraped news from hailiya.com.au
scrape_full_articles.py  ← Python script for scraping full article content
```

---

## How to Deploy the Website

1. Connect to cPanel via FTP (or use cPanel File Manager)
2. Upload the entire contents of the `netlify_deploy/` folder to the `public_html/` directory (or whichever folder the domain points to)
3. The site is static HTML — no server-side setup needed

**Do NOT upload:**
- The `Unzipped Hailiya Rope Photos/` folder (raw photos, not needed for deployment)
- Any `.py` or `.js` scripts from the root folder
- The `node_modules/` folder

---

## What Has Been Done

- Full product catalogue built across 4 sections: Marine (16 products), Defence (12 products), Safety (10 products), Outdoor (5 products)
- All product images matched to source PDFs (marine.pdf, defence.pdf, safety.pdf)
- Product card hover system with modal popups showing full specs
- News section with 119 articles, pagination, and category filtering
- LinkedIn link updated to: https://www.linkedin.com/company/qingdao-hailiya-group-co-ltd/
- Product images upgraded with real Hailiya product photography

---

## What Still Needs to Be Done

### Priority 1 — Sanity CMS Integration (Backend for Admins)

This is the main outstanding task. The website currently has all product and news data hardcoded in `index.html`. The plan is to move this to a Sanity CMS so the client can update content without touching code.

**The full plan and Claude Code prompts are ready.** Ask the outgoing developer (Vedant) for the conversation history, which contains 7 precise prompts to complete this integration. The steps are:

1. Create a Sanity account at https://www.sanity.io (free)
2. Run `npm create sanity@latest` to initialise the studio project
3. Create Product and News schemas (prompts include full code)
4. Run `import-products.js` to migrate all 43 products into Sanity
5. Run `import-news.js` to migrate all news articles into Sanity
6. Deploy the Sanity Studio: `npx sanity deploy`
7. Update `index.html` to fetch data from Sanity API instead of hardcoded HTML

Once done, the client admin logs in at `https://hailiya-group.sanity.studio` to update products/news.

### Priority 2 — Data Verification

Some product modal popups may still show incomplete data (specs table). The `PRODUCT_SPECS` JavaScript object in `index.html` (around line 1821) contains the full modal data. Cross-check entries against:
- `marine.pdf`
- `defence.pdf`
- `safety.pdf`
- `【2026中英文压缩版】蛟龙应急救援产品手册.pdf` (Jiaolong Chinese manual — image-based, no extractable text)

These PDFs are too large to include in this zip. Request them from Vedant or the supervisor via Google Drive.

### Priority 3 — Product Descriptions

Many product cards have placeholder or minimal descriptions. These should be filled in with accurate technical descriptions based on the PDFs.

---

## Key Files in index.html

| What | Where in index.html |
|------|-------------------|
| Product card HTML (Marine) | Line ~795 |
| Product card HTML (Defence) | Line ~1051 |
| Product card HTML (Safety) | Line ~1244 |
| Product card HTML (Outdoor) | Line ~1405 |
| `PRODUCT_SPECS` object (modal data) | Line ~1821 |
| Card-building JS loop | Line ~1973 |
| `openModal()` function | Line ~2100 |
| News data + rendering JS | Search `_naAllData` |

---

## Reference PDFs (Share Separately — Too Large for Zip)

These must be obtained from Vedant or the supervisor via Google Drive:

| File | Size | Purpose |
|------|------|---------|
| `marine.pdf` | ~600MB | Source of truth for all Marine products |
| `defence.pdf` | ~600MB | Source of truth for all Defence products |
| `safety.pdf` | ~600MB | Source of truth for all Safety products |
| `安全领域产品册整套英文版0815.pdf` | ~600MB | English safety products catalog |
| `【2026中英文压缩版】蛟龙应急救援产品手册.pdf` | ~54MB | Jiaolong Chinese manual (image-based, no text) |
| `Hailiya_Product_Specs 24_04.docx.pdf` | — | Product specs reference |

---

## Contacts

- **Client:** Hailiya Group Australia
- **Live LinkedIn:** https://www.linkedin.com/company/qingdao-hailiya-group-co-ltd/
- **Original website (reference):** https://www.hailiya.com.au

---

## Node.js Setup (for Sanity import scripts)

```bash
cd <project-root>
npm install
# Then follow the Sanity integration prompts
```

Requires Node.js 18+.
