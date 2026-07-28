import time
import feedparser
import httpx
from datetime import datetime, timezone
from typing import List, Dict

NICHE_SUBREDDITS = [
    "smallbusiness",
    "entrepreneur",
    "Entrepreneur",
    "automation",
    "business",
    "operations",
    "productivity",
    "sysadmin",
    "nocode",
    "zapier",
]

NICHE_KEYWORDS = [
    "founder", "small business", "manual work", "workflow", "operations",
    "automation", "sop", "burnout", "delegation", "process", "efficiency",
    "outsourcing", "scaling", "smb", "systems", "bottleneck", "overhead",
    "admin", "repetitive", "streamline",
]


def _score_relevance(text: str, keywords: list = None) -> float:
    kws = keywords or NICHE_KEYWORDS
    text_lower = text.lower()
    hits = sum(1 for kw in kws if kw in text_lower)
    return min(hits / 3.0, 1.0)


def _parse_feed(url: str, source_label: str, keywords: list = None) -> List[Dict]:
    try:
        feed = feedparser.parse(url)
    except Exception:
        return []

    items = []
    for entry in feed.entries[:25]:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        combined = f"{title} {summary}"

        relevance = _score_relevance(combined, keywords)
        if relevance == 0:
            continue

        comments = 0
        score = 0

        published = entry.get("published_parsed")
        if published:
            ts = datetime(*published[:6], tzinfo=timezone.utc)
            age_hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
        else:
            age_hours = 24

        items.append({
            "title": title,
            "url": entry.get("link", ""),
            "source": source_label,
            "platform": "reddit",
            "text": summary[:500],
            "relevance": relevance,
            "age_hours": round(age_hours, 1),
            "raw_score": score,
            "comment_count": comments,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        })

    return items


def _fetch_json_listing(subreddit: str, keywords: list = None) -> List[Dict]:
    """Fallback: use .json endpoint with proper headers."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"
    headers = {"User-Agent": "RCC-ContentScanner/1.0 (personal research tool)"}
    try:
        resp = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        if resp.status_code != 200:
            return []
        data = resp.json()
        posts = data.get("data", {}).get("children", [])
        items = []
        for post in posts:
            p = post.get("data", {})
            title = p.get("title", "")
            selftext = p.get("selftext", "")
            combined = f"{title} {selftext}"
            relevance = _score_relevance(combined, keywords)
            if relevance == 0:
                continue
            created = p.get("created_utc", 0)
            ts = datetime.fromtimestamp(created, tz=timezone.utc)
            age_hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
            items.append({
                "title": title,
                "url": f"https://reddit.com{p.get('permalink', '')}",
                "source": f"r/{subreddit}",
                "platform": "reddit",
                "text": selftext[:500] if selftext else title,
                "relevance": relevance,
                "age_hours": round(age_hours, 1),
                "raw_score": p.get("score", 0),
                "comment_count": p.get("num_comments", 0),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })
        return items
    except Exception:
        return []


def fetch(max_subreddits: int = 6, subreddits: list = None, keywords: list = None) -> List[Dict]:
    global NICHE_KEYWORDS
    active_keywords = keywords or NICHE_KEYWORDS
    subs = (subreddits or NICHE_SUBREDDITS)[:max_subreddits]
    results = []
    for i, sub in enumerate(subs):
        if i > 0:
            time.sleep(1.5)
        items = _fetch_json_listing(sub, active_keywords)
        if not items:
            rss_url = f"https://www.reddit.com/r/{sub}/hot.rss"
            items = _parse_feed(rss_url, f"r/{sub}", active_keywords)
        results.extend(items)
    return results
