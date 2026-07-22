import math
import re
from collections import Counter


HIGH = {"war": 14, "closure": 18, "attack": 16, "blockade": 18, "missile": 15, "sanctions": 11, "escalation": 12}
MEDIUM = {"tension": 7, "delay": 6, "rerouting": 7, "disruption": 9, "warning": 5, "premium": 5, "military": 8, "risk": 3}
CALMING = {"normal": -5, "operational": -4, "agreement": -8, "ceasefire": -12, "stable": -5, "resumed": -6}


def score_articles(articles: list[dict]) -> dict:
    counts: Counter[str] = Counter()
    contributions = []
    raw = 18.0
    for article in articles:
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        tokens = re.findall(r"[a-z]+", text)
        local = 0
        for token in tokens:
            weight = HIGH.get(token, MEDIUM.get(token, CALMING.get(token, 0)))
            if weight:
                counts[token] += 1
                local += weight
        raw += min(local, 35) * 0.72
        contributions.append({"title": article.get("title", ""), "signal": round(local, 1)})
    # Smooth saturation avoids brittle 100 scores while remaining explainable.
    score = round(100 / (1 + math.exp(-(raw - 45) / 14)))
    level = "critical" if score >= 80 else "high" if score >= 60 else "elevated" if score >= 35 else "low"
    drivers = [{"term": term, "mentions": count, "weight": HIGH.get(term, MEDIUM.get(term, CALMING.get(term, 0)))} for term, count in counts.most_common(5)]
    confidence = min(0.95, 0.55 + len(articles) * 0.07 + len(counts) * 0.02)
    return {"risk_score": score, "level": level, "confidence": round(confidence, 2), "drivers": drivers, "article_signals": contributions}
