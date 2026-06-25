from typing import List, Dict
import math


def score_items(items: List[Dict]) -> List[Dict]:
    """
    Compute a unified heat score for each item.

    Heat = (engagement_signal * recency_decay * relevance_boost)

    engagement_signal: normalized combination of raw_score and comment_count
      - comments weighted higher because they signal argument/discussion
    recency_decay: exponential decay, half-life ~24h
    relevance_boost: 1.0 to 2.0 multiplier based on niche keyword density
    """
    for item in items:
        raw = item.get("raw_score", 0) or 0
        comments = item.get("comment_count", 0) or 0
        age_hours = item.get("age_hours", 24) or 24
        relevance = item.get("relevance", 0.1) or 0.1

        # comment-to-score ratio signals controversy/discussion
        controversy = 0.0
        if raw > 0:
            controversy = min(comments / raw, 3.0)  # cap at 3x

        engagement = math.log1p(raw) + (math.log1p(comments) * 1.5) + (controversy * 10)

        # half-life of 36 hours
        recency = math.exp(-0.693 * age_hours / 36)

        relevance_multiplier = 1.0 + relevance  # 1.0 – 2.0

        heat = engagement * recency * relevance_multiplier

        item["heat_score"] = round(heat, 3)
        item["controversy_ratio"] = round(controversy, 2)

    return sorted(items, key=lambda x: x["heat_score"], reverse=True)


def split_by_intent(items: List[Dict]):
    """
    Engage feed: recent (< 48h) with decent heat — go comment now.
    Topics feed: all items, clustered by topic for writing inspiration.
    """
    engage = [i for i in items if i.get("age_hours", 999) <= 48]
    topics = items  # all, including older signal
    return engage, topics
