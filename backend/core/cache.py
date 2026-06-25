import sqlite3
import json
import time
from pathlib import Path
from typing import Optional, List, Dict

DB_PATH = Path(__file__).parent.parent.parent / "data" / "cache.db"
CACHE_TTL = 7200  # 2 hours


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scan_cache (
            key TEXT PRIMARY KEY,
            payload TEXT NOT NULL,
            expires_at REAL NOT NULL
        )
    """)
    conn.commit()
    return conn


def get(key: str) -> Optional[List[Dict]]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT payload, expires_at FROM scan_cache WHERE key = ?", (key,)
        ).fetchone()
        if row and row[1] > time.time():
            return json.loads(row[0])
    return None


def set(key: str, data: List[Dict], ttl: int = CACHE_TTL) -> None:
    payload = json.dumps(data)
    expires_at = time.time() + ttl
    with _conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO scan_cache (key, payload, expires_at) VALUES (?, ?, ?)",
            (key, payload, expires_at),
        )
        conn.commit()


def clear() -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM scan_cache")
        conn.commit()
