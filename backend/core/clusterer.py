from typing import List, Dict
import re
from collections import defaultdict

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "be", "been", "have",
    "has", "had", "do", "does", "did", "will", "would", "could", "should",
    "i", "my", "we", "our", "you", "your", "it", "its", "this", "that",
    "how", "what", "when", "why", "who", "which", "not", "no", "so", "just",
    "can", "get", "got", "need", "want", "make", "like", "use", "using",
    "more", "any", "all", "as", "up", "out", "if", "than", "then", "about",
}

TOPIC_SEEDS = {
    "automation": ["automat", "bot", "script", "zapier", "workflow", "trigger", "integrat"],
    "burnout & founder health": ["burnout", "overwhelm", "stress", "exhausted", "founder", "burden", "mental"],
    "delegation & hiring": ["delegat", "hire", "outsourc", "va ", "virtual assistant", "team"],
    "systems & SOPs": ["sop", "system", "process", "document", "checklist", "standard"],
    "scaling & growth": ["scal", "grow", "revenue", "client", "expand", "bottleneck"],
    "tools & software": ["tool", "software", "app", "saas", "platform", "crm", "erp", "notion"],
    "time & productivity": ["time", "productiv", "efficien", "priorit", "focus", "distract"],
    "operations": ["operat", "admin", "overhead", "back office", "manual", "repetit"],
}


def _tokenize(text: str) -> set:
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    return {w for w in words if w not in STOP_WORDS}


def _assign_topic(item: Dict) -> str:
    combined = f"{item.get('title', '')} {item.get('text', '')}".lower()
    best_topic = "general"
    best_hits = 0
    for topic, seeds in TOPIC_SEEDS.items():
        hits = sum(1 for seed in seeds if seed in combined)
        if hits > best_hits:
            best_hits = hits
            best_topic = topic
    return best_topic


def cluster(items: List[Dict]) -> List[Dict]:
    """
    Group items by topic cluster. Returns a flat list with 'topic' field added,
    sorted so items of the same topic are adjacent and clusters ordered by
    aggregate heat.
    """
    topic_heat: Dict[str, float] = defaultdict(float)
    for item in items:
        topic = _assign_topic(item)
        item["topic"] = topic
        topic_heat[topic] += item.get("heat_score", 0)

    # sort items: by topic aggregate heat desc, then individual heat desc
    return sorted(
        items,
        key=lambda x: (topic_heat.get(x["topic"], 0), x.get("heat_score", 0)),
        reverse=True,
    )


def get_topic_summaries(items: List[Dict]) -> List[Dict]:
    """Aggregate stats per topic for the Topics tab."""
    buckets: Dict[str, List[Dict]] = defaultdict(list)
    for item in items:
        buckets[item.get("topic", "general")].append(item)

    summaries = []
    for topic, bucket in buckets.items():
        total_heat = sum(i.get("heat_score", 0) for i in bucket)
        platforms = list({i.get("platform") for i in bucket})
        top_items = sorted(bucket, key=lambda x: x.get("heat_score", 0), reverse=True)[:5]
        summaries.append({
            "topic": topic,
            "total_heat": round(total_heat, 2),
            "post_count": len(bucket),
            "platforms": platforms,
            "top_items": top_items,
        })

    return sorted(summaries, key=lambda x: x["total_heat"], reverse=True)
