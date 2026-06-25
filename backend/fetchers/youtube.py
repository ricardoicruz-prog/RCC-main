import httpx
from datetime import datetime, timezone
from typing import List, Dict, Optional

YT_API = "https://www.googleapis.com/youtube/v3"

SEARCH_QUERIES = [
    "small business automation 2024",
    "founder burnout entrepreneur",
    "business operations systems",
    "workflow automation small business",
    "business process improvement SMB",
    "entrepreneur manual work delegation",
    "small business productivity systems",
]

NICHE_KEYWORDS = [
    "founder", "small business", "manual", "workflow", "operations",
    "automation", "burnout", "delegation", "process", "efficiency",
    "outsourcing", "scaling", "systems", "bottleneck", "admin",
    "repetitive", "streamline", "consultant", "entrepreneur", "owner",
    "sop", "productivity", "time", "overhead",
]


def _score_relevance(text: str) -> float:
    text_lower = text.lower()
    hits = sum(1 for kw in NICHE_KEYWORDS if kw in text_lower)
    return min(hits / 2.0, 1.0)


def _iso_to_age_hours(iso: str) -> float:
    try:
        ts = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - ts).total_seconds() / 3600
    except Exception:
        return 72


def _search_videos(client: httpx.Client, query: str, api_key: str) -> List[Dict]:
    try:
        resp = client.get(
            f"{YT_API}/search",
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "order": "relevance",
                "publishedAfter": "2024-01-01T00:00:00Z",
                "maxResults": 10,
                "key": api_key,
            },
            timeout=10,
        )
        if resp.status_code != 200:
            return []
        return resp.json().get("items", [])
    except Exception:
        return []


def _get_video_stats(client: httpx.Client, video_ids: List[str], api_key: str) -> Dict[str, Dict]:
    if not video_ids:
        return {}
    try:
        resp = client.get(
            f"{YT_API}/videos",
            params={
                "part": "statistics,contentDetails",
                "id": ",".join(video_ids),
                "key": api_key,
            },
            timeout=10,
        )
        if resp.status_code != 200:
            return {}
        stats = {}
        for item in resp.json().get("items", []):
            vid_id = item["id"]
            s = item.get("statistics", {})
            stats[vid_id] = {
                "views": int(s.get("viewCount", 0)),
                "likes": int(s.get("likeCount", 0)),
                "comments": int(s.get("commentCount", 0)),
            }
        return stats
    except Exception:
        return {}


def _get_transcript_excerpt(video_id: str) -> str:
    """Pull first ~300 words of transcript to extract quotable content."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        words = " ".join(seg["text"] for seg in transcript[:40])
        return words[:500]
    except Exception:
        return ""


def fetch(api_key: str, max_queries: int = 4) -> List[Dict]:
    if not api_key:
        return []

    results = []
    seen_ids = set()

    with httpx.Client() as client:
        for query in SEARCH_QUERIES[:max_queries]:
            items = _search_videos(client, query, api_key)
            video_ids = []
            for item in items:
                vid_id = item.get("id", {}).get("videoId", "")
                if vid_id and vid_id not in seen_ids:
                    seen_ids.add(vid_id)
                    video_ids.append(vid_id)

            stats_map = _get_video_stats(client, video_ids, api_key)

            for item in items:
                vid_id = item.get("id", {}).get("videoId", "")
                if not vid_id:
                    continue
                snippet = item.get("snippet", {})
                title = snippet.get("title", "")
                description = snippet.get("description", "")
                channel = snippet.get("channelTitle", "")
                published = snippet.get("publishedAt", "")

                combined = f"{title} {description}"
                relevance = _score_relevance(combined)
                if relevance == 0:
                    continue

                age_hours = _iso_to_age_hours(published)
                stats = stats_map.get(vid_id, {})
                views = stats.get("views", 0)
                likes = stats.get("likes", 0)
                comment_count = stats.get("comments", 0)

                # try to get transcript excerpt for high-relevance videos
                transcript_text = ""
                if relevance >= 0.5 and views > 500:
                    transcript_text = _get_transcript_excerpt(vid_id)

                text = transcript_text or description[:500]

                results.append({
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                    "source": f"YouTube – {channel}",
                    "platform": "youtube",
                    "text": text,
                    "relevance": relevance,
                    "age_hours": round(age_hours, 1),
                    "raw_score": likes + (views // 100),  # normalize views to like-scale
                    "comment_count": comment_count,
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                })

    return results
