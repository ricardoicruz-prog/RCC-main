# RCC – Research & Content Commander

Social media content intelligence tool for small business consultants.
Scans Reddit, Hacker News, and Bluesky for hot posts relevant to the
"small business operations & automation" niche.

## Running locally

```bash
pip install -r requirements.txt
python run.py
```

Opens at http://localhost:8000. Results cached 2 hours in `data/cache.db`.

## Project structure

```
backend/
  main.py              FastAPI app + API routes
  fetchers/
    reddit.py          Reddit .json API + RSS fallback
    hackernews.py      HN Firebase public API
    bluesky.py         AT Protocol public search
  core/
    scorer.py          Heat scoring (engagement * recency * relevance)
    clusterer.py       Topic clustering by keyword seeds
    cache.py           SQLite-backed 2-hour cache
frontend/
  templates/index.html Single-page UI
  static/css/app.css
  static/js/app.js
run.py                 Entry point (opens browser automatically)
```

## Environment variables

Copy `.env.example` to `.env` to set Bluesky credentials server-side:

```
BLUESKY_HANDLE=yourname.bsky.social
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

## Notes on rate limits

- Reddit: 1 request per subreddit with 1.5s pacing between fetches
- HN Firebase: no rate limits, fully public
- Bluesky: 5 search queries per scan, public API used
