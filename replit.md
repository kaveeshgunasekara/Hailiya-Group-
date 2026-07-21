# Hailiya Group Australia — Corporate Website

## Project overview

Static HTML website for Hailiya Group Australia, the Australian distributor for Qingdao Huakai Ocean Science & Technology. Showcases rope products across four categories (Marine, Defence, Safety, Outdoor) and displays company news.

All product and news data is fetched at runtime from **Sanity CMS** (project ID: `15fxxqgw`, dataset: `production`). Confirmed live data: **43 products** and **119 news articles**.

## Stack

- **Frontend:** Single-page static HTML (`netlify_deploy/index.html`) with inline CSS and JS
- **Dev server:** `server.js` — serves static files from `netlify_deploy/` and proxies Sanity API calls server-side (no CORS issues in preview)
- **CMS:** Sanity (`15fxxqgw` / `production`) — products and news fetched via `/sanity-proxy` → `apicdn.sanity.io`
- **Deployment target:** cPanel (upload contents of `netlify_deploy/`) or Netlify
- **Sanity Studio:** https://hailiya-group.sanity.studio

## How to run on Replit

```bash
node server.js
```

The "Start application" workflow runs this automatically on port 5000. Products and news load correctly in the Replit preview via the server-side Sanity proxy.

## Folder structure

```
netlify_deploy/          ← The live website (deploy this folder to cPanel/Netlify)
  index.html             ← Main site (all sections, JS, CSS inline)
  news-article.html      ← Individual news article page
  privacy.html           ← Privacy policy
  images/                ← All images (products, news thumbnails)
  videos/                ← Video assets
  robots.txt / sitemap.xml
server.js                ← Replit dev server: static files + Sanity proxy at /sanity-proxy
scripts/post-merge.sh    ← Post-merge setup script (runs npm install)
import-products.js       ← One-time Sanity import script (43 products) — already run
import-news.js           ← One-time Sanity import script (119 news articles) — already run
HANDOVER.md              ← Full handover notes from outgoing developer
```

## Key locations in index.html

| What | Location |
|------|----------|
| Sanity config (project ID, dataset) | Line ~1879 |
| `sanityFetch()` — calls `/sanity-proxy` | Line ~1883 |
| `loadProductsFromSanity()` | Line ~1906 |
| `loadNewsFromSanity()` | Line ~1926 |
| Product card HTML (Marine) | Line ~795 |
| `PRODUCT_SPECS` modal data | Line ~1821 |

## Sanity CMS

- **Project ID:** `15fxxqgw`
- **Dataset:** `production`
- **Studio:** https://hailiya-group.sanity.studio
- **Data confirmed:** 43 products, 119 news articles
- **Images:** hosted on `cdn.sanity.io`

> Note: The `netlify_deploy/index.html` CSP and `netlify.toml` do not include the Sanity CDN in `connect-src` — this doesn't matter for Replit (proxy handles it) but should be checked if deploying directly to Netlify.

## Contacts

- **Client:** Hailiya Group Australia
- **Live site:** https://www.hailiya.com.au
- **LinkedIn:** https://www.linkedin.com/company/qingdao-hailiya-group-co-ltd/
- **Outgoing developer:** Vedant

## User preferences
