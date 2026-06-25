import httpx
from datetime import datetime, timezone
from typing import List, Dict, Optional

BSKY_API = "https://public.api.bsky.app/xrpc"

SEARCH_QUERIES = [
    "small business automation",
    "founder burnout",
    "business operations",
    "workflow automation SMB",
    "manual processes small business",
    "business systems founder",
    "process improvement entrepreneur",
    "delegation small business",
]

NICHE_KEYWORDS = [
    "founder", "small business", "manual", "workflow", "operations",
    "automation", "burnout", "delegation", "process", "efficiency",
    "outsourcing", "scaling", "systems", "bottleneck", "admin",
    "repetitive", "streamline", "consultant",
]


def _score_relevance(text: str) -> float:
    text_lower = text.lower()
    hits = sum(1 for kw in NICHE_KEYWORDS if kw in text_lower)
    return min(hits / 2.0, 1.0)


def _search_posts(client: httpx.Client, query: str, token: Optional[str] = None) -> List[Dict]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = client.get(
            f"{BSKY_API}/app.bsky.feed.searchPosts",
            params={"q": query, "limit": 20, "sort": "top"},
            headers=headers,
            timeout=10,
        )
        if resp.status_code != 200:
            return []
        return resp.json().get("posts", [])
    except Exception:
        return []


def _get_auth_token(handle: str, app_password: str) -> Optional[str]:
    try:
        resp = httpx.post(
            f"{BSKY_API}/com.atproto.server.createSession",
            json={"identifier": handle, "password": app_password},
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json().get("accessJwt")
    except Exception:
        pass
    return None


def fetch(handle: Optional[str] = None, app_password: Optional[str] = None) -> List[Dict]:
    token = None
    if handle and app_password:
        token = _get_auth_token(handle, app_password)

    results = []
    seen_uris = set()

    with httpx.Client() as client:
        for query in SEARCH_QUERIES[:5]:  # cap at 5 queries to stay polite
            posts = _search_posts(client, query, token)
            for post in posts:
                uri = post.get("uri", "")
                if uri in seen_uris:
                    continue
                seen_uris.add(uri)

                record = post.get("record", {})
                text = record.get("text", "")
                relevance = _score_relevance(text)
                if relevance == 0:
                    continue

                created_at = record.get("createdAt", "")
                try:
                    ts = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    age_hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
                except Exception:
                    age_hours = 24

                # build web URL from AT URI
                parts = uri.replace("at://", "").split("/")
                did = parts[0] if parts else ""
                rkey = parts[-1] if len(parts) > 2 else ""
                author = post.get("author", {})
                author_handle = author.get("handle", did)
                web_url = f"https://bsky.app/profile/{author_handle}/post/{rkey}"

                like_count = post.get("likeCount", 0)
                reply_count = post.get("replyCount", 0)
                repost_count = post.get("repostCount", 0)

                results.append({
                    "title": text[:100] + ("..." if len(text) > 100 else ""),
                    "url": web_url,
                    "source": f"Bluesky @{author_handle}",
                    "platform": "bluesky",
                    "text": text[:500],
                    "relevance": relevance,
                    "age_hours": round(age_hours, 1),
                    "raw_score": like_count + repost_count,
                    "comment_count": reply_count,
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                })

    return results
