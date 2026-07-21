"""
scrape_full_articles.py
Scrapes full article content from https://www.huakai-rope.com/news.html
and updates _naAllData in both index.html and news-article.html.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import json
import os

BASE = "https://www.huakai-rope.com"
NEWS_URL = "https://www.huakai-rope.com/news.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}
HAILI_DIR = r"C:\Users\vedan\Desktop\Haili"

# ─────────────────────────────────────────────────────────────
# TASK 1 — Collect all article links (handle pagination)
# ─────────────────────────────────────────────────────────────
def get_all_article_links():
    article_links = []
    visited_pages = set()
    pages_to_visit = [NEWS_URL]

    while pages_to_visit:
        page_url = pages_to_visit.pop(0)
        if page_url in visited_pages:
            continue
        visited_pages.add(page_url)

        try:
            r = requests.get(page_url, headers=HEADERS, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print(f"  [!] Failed to fetch page {page_url}: {e}")
            continue

        soup = BeautifulSoup(r.text, "html.parser")

        # Find article links — look for links containing /news/index
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            # Match article URLs like /news/index123.html or news/index123.html
            if re.search(r'news/index\d+', href):
                full_url = href if href.startswith("http") else BASE + ("/" if not href.startswith("/") else "") + href
                # Normalise
                full_url = full_url.split("?")[0].strip()
                if full_url not in [x[0] for x in article_links]:
                    # Extract id from URL
                    m = re.search(r'(index\d+)', full_url)
                    art_id = m.group(1) if m else None
                    article_links.append((full_url, art_id))

        # Find pagination links
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            # Look for next-page patterns: ?page=2, /news_2.html, /news/2, etc.
            if re.search(r'(page=\d+|news_\d+\.html|/news/\d+)', href) or \
               (("news" in href) and re.search(r'\d+', href) and "index" not in href):
                full_url = href if href.startswith("http") else BASE + ("/" if not href.startswith("/") else "") + href
                if full_url not in visited_pages and full_url not in pages_to_visit:
                    # Only add if it looks like a list page (not an article)
                    if not re.search(r'news/index\d+', full_url):
                        pages_to_visit.append(full_url)

        print(f"  Page {page_url} → {len(article_links)} articles found so far")
        time.sleep(0.5)

    print(f"\nTASK 1 COMPLETE: {len(article_links)} article links found\n")
    return article_links


# ─────────────────────────────────────────────────────────────
# TASK 2 — Fetch full content for every article
# ─────────────────────────────────────────────────────────────
def fetch_article(url, art_id):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or "utf-8"
    except Exception as e:
        return None, str(e)

    soup = BeautifulSoup(r.text, "html.parser")

    # ── Title ──────────────────────────────────────────────────
    title = ""
    for sel in ["h1", ".article-title", ".news-title", ".detail-title", ".title"]:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            title = el.get_text(strip=True)
            break
    if not title:
        og = soup.find("meta", property="og:title")
        if og:
            title = og.get("content", "").strip()

    # ── Date ───────────────────────────────────────────────────
    date = ""
    for sel in [".date", ".time", ".article-date", ".news-date", ".pub-date", "time"]:
        el = soup.select_one(sel)
        if el:
            text = el.get("datetime", "") or el.get_text(strip=True)
            m = re.search(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}", text)
            if m:
                date = m.group().replace("/", "-")
                break

    # ── Category ───────────────────────────────────────────────
    category = ""
    for sel in [".category", ".tag", ".article-category", ".breadcrumb a"]:
        el = soup.select_one(sel)
        if el:
            category = el.get_text(strip=True)
            break

    # ── Main image ─────────────────────────────────────────────
    img_url = ""
    og_img = soup.find("meta", property="og:image")
    if og_img:
        img_url = og_img.get("content", "")
    if not img_url:
        for sel in [".article-img img", ".detail-img img", ".news-img img", "article img", ".content img"]:
            el = soup.select_one(sel)
            if el and el.get("src"):
                src = el["src"]
                img_url = src if src.startswith("http") else BASE + ("/" if not src.startswith("/") else "") + src
                break

    # ── Body content ───────────────────────────────────────────
    # Try various common content containers
    body_html = ""
    content_el = None
    for sel in [
        ".article-content", ".article-body", ".detail-content", ".detail-body",
        ".news-content", ".news-body", ".content-main", ".main-content",
        "article .content", ".article", "#article-body", ".post-content",
        ".entry-content", "[class*='content']", "[class*='detail']"
    ]:
        el = soup.select_one(sel)
        if el:
            # Make sure it has meaningful text (>50 chars)
            text = el.get_text(strip=True)
            if len(text) > 50:
                content_el = el
                break

    if content_el is None:
        # Fallback: find the main div with most text
        divs = soup.find_all("div")
        max_len = 0
        for div in divs:
            t = div.get_text(strip=True)
            if len(t) > max_len:
                max_len = len(t)
                content_el = div

    if content_el:
        # Build clean HTML preserving structure
        body_parts = []
        for el in content_el.find_all(["p", "h1", "h2", "h3", "h4", "strong", "b", "ul", "ol", "li", "br"]):
            tag = el.name
            text = el.get_text(strip=True)
            if not text:
                continue
            if tag in ["h2", "h3", "h4"]:
                body_parts.append(f"<{tag}>{text}</{tag}>")
            elif tag in ["strong", "b"]:
                pass  # handled by parent p
            elif tag in ["ul", "ol"]:
                items = [f"<li>{li.get_text(strip=True)}</li>" for li in el.find_all("li") if li.get_text(strip=True)]
                if items:
                    body_parts.append(f"<{tag}>{''.join(items)}</{tag}>")
            elif tag == "p":
                # Preserve inner bold/strong/em
                inner = ""
                for child in el.children:
                    if hasattr(child, "name"):
                        if child.name in ["strong", "b"]:
                            inner += f"<strong>{child.get_text(strip=True)}</strong>"
                        elif child.name == "em":
                            inner += f"<em>{child.get_text(strip=True)}</em>"
                        elif child.name == "a":
                            inner += child.get_text(strip=True)
                        elif child.name == "br":
                            inner += "<br>"
                        else:
                            inner += child.get_text(strip=True)
                    else:
                        inner += str(child)
                inner = inner.strip()
                if inner:
                    body_parts.append(f"<p>{inner}</p>")

        # Deduplicate consecutive identical elements
        seen = []
        for part in body_parts:
            if not seen or part != seen[-1]:
                seen.append(part)
        body_html = "\n".join(seen)

        # If body is still empty/short, just use the raw text wrapped in <p>
        if len(body_html.strip()) < 100:
            raw_text = content_el.get_text(separator="\n", strip=True)
            paragraphs = [p.strip() for p in raw_text.split("\n") if len(p.strip()) > 30]
            body_html = "\n".join(f"<p>{p}</p>" for p in paragraphs)

    return {
        "id": art_id,
        "url": url,
        "title": title,
        "date": date,
        "category": category,
        "img_url": img_url,
        "body_html": body_html,
    }, None


def fetch_all_articles(article_links):
    results = []
    failed = []
    total = len(article_links)

    for i, (url, art_id) in enumerate(article_links, 1):
        art, err = fetch_article(url, art_id)
        if art:
            results.append(art)
        else:
            failed.append({"url": url, "id": art_id, "error": err})
            print(f"  [!] FAILED: {url} → {err}")

        if i % 10 == 0 or i == total:
            print(f"  Fetched {i}/{total}...")

        time.sleep(0.5)

    print(f"\nTASK 2 COMPLETE: {len(results)} articles fetched, {len(failed)} failed\n")
    return results, failed


# ─────────────────────────────────────────────────────────────
# TASK 3 — Read current _naAllData from news-article.html
# ─────────────────────────────────────────────────────────────
def read_na_all_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    m = re.search(r'var _naAllData\s*=\s*(\[[\s\S]*?\]);', content)
    if not m:
        raise ValueError(f"_naAllData not found in {filepath}")

    data_str = m.group(1)
    data = json.loads(data_str)
    print(f"TASK 3: {len(data)} articles in _naAllData of {os.path.basename(filepath)}\n")
    return content, data, m


# ─────────────────────────────────────────────────────────────
# TASK 4 — Match scraped articles to _naAllData and add body
# ─────────────────────────────────────────────────────────────
def normalize(s):
    return re.sub(r"\s+", " ", str(s).lower().strip())

def match_articles(na_data, scraped):
    # Build lookup by art_id
    scraped_by_id = {art["id"]: art for art in scraped if art["id"]}
    # Build lookup by normalized title
    scraped_by_title = {}
    for art in scraped:
        if art["title"]:
            scraped_by_title[normalize(art["title"])] = art

    matched = 0
    unmatched = []
    updated_data = []

    for row in na_data:
        row = list(row)  # make mutable
        art_id = row[0]   # e.g. "index167"
        title  = row[1]
        date   = row[2]
        # row[3] = excerpt, row[4] = category

        # Ensure we have index 5 slot
        while len(row) < 6:
            row.append("")

        # Try match by ID first
        scraped_art = scraped_by_id.get(art_id)

        # Try match by normalized title
        if not scraped_art:
            scraped_art = scraped_by_title.get(normalize(title))

        if scraped_art and scraped_art.get("body_html") and len(scraped_art["body_html"].strip()) > 50:
            row[5] = scraped_art["body_html"]
            # Update excerpt with first full paragraph if available
            first_p = re.search(r"<p>(.*?)</p>", scraped_art["body_html"], re.DOTALL)
            if first_p:
                first_text = re.sub(r"<[^>]+>", "", first_p.group(1)).strip()
                if len(first_text) > len(row[3]):
                    row[3] = first_text[:500]  # cap excerpt at 500 chars
            matched += 1
        else:
            unmatched.append({"id": art_id, "title": title})

        updated_data.append(row)

    print(f"TASK 4: {matched}/{len(na_data)} articles matched and updated")
    print(f"  Unmatched: {len(unmatched)}")
    if unmatched:
        for u in unmatched[:10]:
            print(f"    - [{u['id']}] {u['title'][:60]}")
        if len(unmatched) > 10:
            print(f"    ... and {len(unmatched)-10} more")
    print()
    return updated_data, matched, unmatched


# ─────────────────────────────────────────────────────────────
# TASK 5 — Update news-article.html rendering
# ─────────────────────────────────────────────────────────────
BODY_RENDER_OLD = """    // Body — split on ". " into sentences, each as a <p>
    var bodyDiv = document.createElement('div');
    bodyDiv.className = 'art-body';
    var sentences = body.split('. ');
    for (var s = 0; s < sentences.length; s++) {
      var text = sentences[s].trim();
      if (!text) continue;
      // Re-add period if not the last fragment and doesn't already end with punctuation
      if (s < sentences.length - 1 && !/[.!?]$/.test(text)) {
        text += '.';
      }
      var p = document.createElement('p');
      p.textContent = text;
      bodyDiv.appendChild(p);
    }
    wrap.appendChild(bodyDiv);"""

BODY_RENDER_NEW = """    // Body — use full HTML body (a[5]) if available, else split excerpt into sentences
    var bodyDiv = document.createElement('div');
    bodyDiv.className = 'art-body';
    var fullBody = a[5] || '';
    if (fullBody && fullBody.length > 50) {
      bodyDiv.innerHTML = fullBody;
    } else {
      var sentences = body.split('. ');
      for (var s = 0; s < sentences.length; s++) {
        var text = sentences[s].trim();
        if (!text) continue;
        if (s < sentences.length - 1 && !/[.!?]$/.test(text)) {
          text += '.';
        }
        var p = document.createElement('p');
        p.textContent = text;
        bodyDiv.appendChild(p);
      }
    }
    wrap.appendChild(bodyDiv);"""

READTIME_OLD = "  function readTime(text) {\n    return Math.max(1, Math.ceil(text.split(' ').length / 200));\n  }"
READTIME_NEW = "  function readTime(text) {\n    var plain = text.replace(/<[^>]+>/g, ' ');\n    return Math.max(1, Math.ceil(plain.split(' ').length / 200));\n  }"

def update_article_rendering(content):
    if BODY_RENDER_OLD in content:
        content = content.replace(BODY_RENDER_OLD, BODY_RENDER_NEW)
        print("TASK 5: Updated body rendering in news-article.html ✓")
    else:
        print("TASK 5: Body rendering already updated or pattern not found — skipping")
    if READTIME_OLD in content:
        content = content.replace(READTIME_OLD, READTIME_NEW)
    return content


# ─────────────────────────────────────────────────────────────
# TASK 6 — Serialise updated data and save files
# ─────────────────────────────────────────────────────────────
def serialise_data(updated_data):
    """Serialise the updated _naAllData array to a JS-safe string."""
    # Use json.dumps which handles escaping correctly
    return json.dumps(updated_data, ensure_ascii=False)


def update_file(filepath, updated_data, update_render=False):
    content, _, match_obj = read_na_all_data(filepath)

    new_data_str = "var _naAllData = " + serialise_data(updated_data) + ";"

    # Replace the old _naAllData declaration
    old_decl = "var _naAllData = " + match_obj.group(1) + ";"
    if old_decl in content:
        content = content.replace(old_decl, new_data_str)
    else:
        # Try regex replacement
        content = re.sub(
            r'var _naAllData\s*=\s*\[[\s\S]*?\];',
            new_data_str,
            content
        )

    if update_render:
        content = update_article_rendering(content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {filepath}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    index_html      = os.path.join(HAILI_DIR, "index.html")
    article_html    = os.path.join(HAILI_DIR, "news-article.html")

    print("=" * 60)
    print("TASK 1 — Collecting article links from huakai-rope.com")
    print("=" * 60)
    article_links = get_all_article_links()

    print("=" * 60)
    print("TASK 2 — Fetching full content for each article")
    print("=" * 60)
    scraped, failed = fetch_all_articles(article_links)

    print("=" * 60)
    print("TASK 3 — Reading current _naAllData")
    print("=" * 60)
    # Read from news-article.html (same data in both files)
    _, na_data, _ = read_na_all_data(article_html)

    print("=" * 60)
    print("TASK 4 — Matching and updating articles")
    print("=" * 60)
    updated_data, matched, unmatched = match_articles(na_data, scraped)

    print("=" * 60)
    print("TASK 5+6 — Updating news-article.html (render + data)")
    print("=" * 60)
    update_file(article_html, updated_data, update_render=True)

    print("\nUpdating index.html (data only)...")
    update_file(index_html, updated_data, update_render=False)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total articles scraped from source site : {len(article_links)}")
    print(f"  Articles successfully fetched           : {len(scraped)}")
    print(f"  Articles matched + updated              : {matched}")
    print(f"  Articles not matched                    : {len(unmatched)}")
    print(f"  Articles where fetching failed          : {len(failed)}")
    if failed:
        print("\n  Failed URLs:")
        for f in failed:
            print(f"    {f['url']} → {f['error']}")
    print("\nDone!")
