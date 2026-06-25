import httpx
from datetime import datetime, timezone
from typing import List, Dict

FIREBASE_BASE = "https://hacker-news.firebaseio.com/v0"

NICHE_KEYWORDS = [
    "founder", "small business", "manual", "workflow", "operations",
    "automation", "sop", "burnout", "delegation", "process", "efficiency",
    "outsourcing", "scaling", "smb", "systems", "bottleneck", "overhead",
    "admin", "repetitive", "streamline", "productivity", "startup",
    "solopreneur", "consultant", "freelance", "business owner",
]


def _score_relevance(text: str) -> float:
    text_lower = text.lower()
    hits = sum(1 for kw in NICHE_KEYWORDS if kw in text_lower)
    return min(hits / 2.0, 1.0)


def _get_item(client: httpx.Client, item_id: int) -> Dict:
    try:
        resp = client.get(f"{FIREBASE_BASE}/item/{item_id}.json", timeout=8)
        return resp.json() or {}
    except Exception:
        return {}


def fetch(limit: int = 60) -> List[Dict]:
    results = []
    try:
        with httpx.Client() as client:
            resp = client.get(f"{FIREBASE_BASE}/topstories.json", timeout=10)
            top_ids = resp.json()[:limit]

            for item_id in top_ids:
                item = _get_item(client, item_id)
                if not item or item.get("type") != "story":
                    continue

                title = item.get("title", "")
                text = item.get("text", "")
                combined = f"{title} {text}"
                relevance = _score_relevance(combined)
                if relevance == 0:
                    continue

                created = item.get("time", 0)
                ts = datetime.fromtimestamp(created, tz=timezone.utc)
                age_hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600

                url = item.get("url") or f"https://news.ycombinator.com/item?id={item_id}"
                results.append({
                    "title": title,
                    "url": url,
                    "source": "Hacker News",
                    "platform": "hackernews",
                    "text": text[:500] if text else title,
                    "relevance": relevance,
                    "age_hours": round(age_hours, 1),
                    "raw_score": item.get("score", 0),
                    "comment_count": item.get("descendants", 0),
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                })
    except Exception:
        pass
    return results
