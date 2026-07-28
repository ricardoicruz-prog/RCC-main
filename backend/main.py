import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

from backend.fetchers import reddit, hackernews, bluesky, youtube, firecrawl
from backend.core import scorer, clusterer, cache, industries

app = FastAPI(title="RCC – Research & Content Commander")

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")


class ScanRequest(BaseModel):
    force_refresh: bool = False
    industry: str = "all"


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = FRONTEND_DIR / "templates" / "index.html"
    return HTMLResponse(html_path.read_text())


@app.get("/api/industries")
async def list_industries():
    return {
        key: {"label": v["label"], "emoji": v["emoji"]}
        for key, v in industries.INDUSTRIES.items()
    }


@app.post("/api/scan")
async def run_scan(req: ScanRequest):
    cache_key = f"scan_v2_{req.industry}"
    if not req.force_refresh:
        cached = cache.get(cache_key)
        if cached:
            return JSONResponse({"status": "cached", "data": cached})

    ind = industries.get_industry(req.industry)
    kw = ind["keywords"]
    subs = ind["subreddits"]
    yt_q = ind["yt_queries"]
    bsky_q = ind["bsky_queries"]

    all_items = []

    reddit_items = reddit.fetch(subreddits=subs, keywords=kw)
    all_items.extend(reddit_items)

    hn_items = hackernews.fetch(keywords=kw)
    all_items.extend(hn_items)

    bsky_handle = os.environ.get("BLUESKY_HANDLE", "")
    bsky_password = os.environ.get("BLUESKY_APP_PASSWORD", "")
    bsky_items = bluesky.fetch(
        handle=bsky_handle or None,
        app_password=bsky_password or None,
        queries=bsky_q,
        keywords=kw,
    )
    all_items.extend(bsky_items)

    yt_key = os.environ.get("YOUTUBE_API_KEY", "")
    if yt_key:
        yt_items = youtube.fetch(api_key=yt_key, queries=yt_q, keywords=kw)
        all_items.extend(yt_items)

    fc_key = os.environ.get("FIRECRAWL_API_KEY", "")
    if fc_key:
        fc_items = firecrawl.fetch(api_key=fc_key)
        all_items.extend(fc_items)

    # tag pain signals
    for item in all_items:
        signal = industries.detect_pain_signal(f"{item.get('title','')} {item.get('text','')}")
        item["pain_signal"] = signal

    scored = scorer.score_items(all_items)
    engage_feed, topics_feed = scorer.split_by_intent(scored)

    clustered_topics = clusterer.cluster(topics_feed)
    topic_summaries = clusterer.get_topic_summaries(clustered_topics)

    result = {
        "engage": engage_feed[:30],
        "topics": topic_summaries[:10],
        "total_fetched": len(all_items),
        "industry": req.industry,
        "industry_label": ind["label"],
        "platform_counts": {
            "reddit": sum(1 for i in all_items if i["platform"] == "reddit"),
            "hackernews": sum(1 for i in all_items if i["platform"] == "hackernews"),
            "bluesky": sum(1 for i in all_items if i["platform"] == "bluesky"),
            "youtube": sum(1 for i in all_items if i["platform"] == "youtube"),
            "firecrawl": sum(1 for i in all_items if i["platform"] == "firecrawl"),
        },
    }

    cache.set(cache_key, result)
    return JSONResponse({"status": "fresh", "data": result})


@app.post("/api/clear-cache")
async def clear_cache():
    cache.clear()
    return {"status": "ok"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
