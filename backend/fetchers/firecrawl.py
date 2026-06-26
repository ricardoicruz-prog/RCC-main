import httpx
from datetime import datetime, timezone
from typing import List, Dict

FIRECRAWL_API = "https://api.firecrawl.dev/v1"

# Industry sites relevant to small business ops & automation
INDUSTRY_SOURCES = [
    {"url": "https://www.inc.com/operations", "label": "Inc. – Operations"},
    {"url": "https://www.entrepreneur.com/topic/systems", "label": "Entrepreneur – Systems"},
    {"url": "https://hbr.org/topic/operations-strategy", "label": "HBR – Operations"},
    {"url": "https://www.process.st/blog", "label": "Process Street Blog"},
    {"url": "https://zapier.com/blog/automation-small-business", "label": "Zapier Blog"},
    {"url": "https://www.score.org/blog", "label": "SCORE – Small Business"},
    {"url": "https://smallbiztrends.com/category/technology", "label": "Small Biz Trends"},
]

NICHE_KEYWORDS = [
    "founder", "small business", "manual", "workflow", "operations",
    "automation", "burnout", "delegation", "process", "efficiency",
    "outsourcing", "scaling", "systems", "bottleneck", "admin",
    "repetitive", "streamline", "consultant", "entrepreneur", "owner",
    "sop", "productivity", "overhead", "10 employees", "50 employees",
]


def _score_relevance(text: str) -> float:
    text_lower = text.lower()
    hits = sum(1 for kw in NICHE_KEYWORDS if kw in text_lower)
    return min(hits / 2.0, 1.0)


def _scrape_url(client: httpx.Client, url: str, api_key: str) -> Dict:
    try:
        resp = client.post(
            f"{FIRECRAWL_API}/scrape",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "url": url,
                "formats": ["markdown"],
                "onlyMainContent": True,
                "waitFor": 1000,
            },
            timeout=20,
        )
        if resp.status_code != 200:
            return {}
        data = resp.json()
        return data.get("data", {})
    except Exception:
        return {}


def _extract_articles(markdown: str, source_url: str, label: str) -> List[Dict]:
    """
    Parse scraped markdown into individual article snippets.
    Looks for heading patterns (## or ###) as article separators.
    """
    if not markdown:
        return []

    import re
    # split on markdown headings
    sections = re.split(r'\n(?=#{1,3} )', markdown)
    articles = []

    for section in sections[:20]:  # cap at 20 sections per source
        lines = section.strip().splitlines()
        if not lines:
            continue

        title_line = lines[0].lstrip('#').strip()
        body = " ".join(lines[1:6]).strip()  # first few lines as excerpt

        if len(title_line) < 15:  # too short to be a real title
            continue

        combined = f"{title_line} {body}"
        relevance = _score_relevance(combined)
        if relevance == 0:
            continue

        articles.append({
            "title": title_line[:200],
            "url": source_url,
            "source": label,
            "platform": "firecrawl",
            "text": body[:500],
            "relevance": relevance,
            "age_hours": 48.0,  # unknown — treat as 2 days old
            "raw_score": 0,
            "comment_count": 0,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        })

    return articles


def fetch(api_key: str, sources: List[Dict] = None) -> List[Dict]:
    if not api_key:
        return []

    sources = sources or INDUSTRY_SOURCES
    results = []

    with httpx.Client() as client:
        for source in sources:
            data = _scrape_url(client, source["url"], api_key)
            markdown = data.get("markdown", "")
            articles = _extract_articles(markdown, source["url"], source["label"])
            results.extend(articles)

    return results
