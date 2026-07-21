# Hailiya Group Australia — Corporate Website

## Project overview

Static HTML website for Hailiya Group Australia, the Australian distributor for Qingdao Huakai Ocean Science & Technology. Showcases rope products across four categories (Marine, Defence, Safety, Outdoor) and displays company news.

The website fetches all product and news data at runtime from **Sanity CMS** (project ID: `15fxxqgw`, dataset: `production`). There is no hardcoded product/news data in the HTML — it is all CMS-driven.

## Stack

- **Frontend:** Single-page static HTML (`netlify_deploy/index.html`) with inline CSS and JS
- **CMS:** Sanity (`15fxxqgw` / `production`) — products and news fetched via public CDN API
- **Deployment target:** cPanel (upload contents of `netlify_deploy/`) or Netlify
- **Sanity Studio:** https://hailiya-group.sanity.studio

## How to run on Replit

```bash
npx --yes serve netlify_deploy -l 5000
```

Workflow "Start application" is configured to do this automatically.

> **Note:** Sanity API calls will fail with a CORS error in the Replit preview because Sanity's CORS settings only allow `hailiya.com.au`. Products and news will not load in the preview — this is expected. On the live site they load correctly.

## Folder structure

```
netlify_deploy/          ← The live website (deploy this folder)
  index.html             ← Main site (all sections, JS, CSS inline)
  news-article.html      ← Individual news article page
  privacy.html           ← Privacy policy
  images/                ← All images (products, news thumbnails)
  videos/                ← Video assets
  robots.txt / sitemap.xml
import-products.js       ← One-time Sanity import script (products)
import-news.js           ← One-time Sanity import script (news)
HANDOVER.md              ← Full handover notes from outgoing developer
```

## Key locations in index.html

| What | Location |
|------|----------|
| Sanity config (project ID, dataset) | Line ~1879 |
| `loadProductsFromSanity()` | Line ~1906 |
| `loadNewsFromSanity()` | Line ~1926 |
| Product card HTML (Marine) | Line ~795 |
| `PRODUCT_SPECS` modal data | Line ~1821 |

## Contacts

- **Client:** Hailiya Group Australia
- **Live site:** https://www.hailiya.com.au
- **LinkedIn:** https://www.linkedin.com/company/qingdao-hailiya-group-co-ltd/
- **Outgoing developer:** Vedant

## User preferences
