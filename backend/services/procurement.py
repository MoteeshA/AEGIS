from __future__ import annotations

import heapq

from backend.data.mock_data import SUPPLIERS


GRAPH = {
    "Saudi Arabia": [("Strait of Hormuz", 620)],
    "UAE": [("Fujairah Bypass", 340), ("Strait of Hormuz", 450)],
    "Fujairah Bypass": [("Bab el-Mandeb", 1550)],
    "Strait of Hormuz": [("Bab el-Mandeb", 1800)],
    "Bab el-Mandeb": [("Suez Canal", 1350), ("Cape of Good Hope", 5200)],
    "Suez Canal": [("Rotterdam", 3300)],
    "Cape of Good Hope": [("Rotterdam", 6200)],
    "Norway": [("Rotterdam", 860)],
    "United States": [("Rotterdam", 3900)],
    "Brazil": [("Rotterdam", 5100)],
    "Nigeria": [("Rotterdam", 4100)],
}


def shortest_route(origin: str, destination: str, blocked: set[str]) -> tuple[list[str], float] | None:
    queue = [(0.0, origin, [origin])]
    seen = set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in seen or node in blocked:
            continue
        seen.add(node)
        if node == destination:
            return path, cost
        for nxt, distance in GRAPH.get(node, []):
            if nxt not in blocked:
                heapq.heappush(queue, (cost + distance, nxt, path + [nxt]))
    return None


def recommend(origin: str, destination: str, blocked_nodes: list[str], required_mbd: float) -> dict:
    blocked = set(blocked_nodes)
    options = []
    for supplier in SUPPLIERS:
        if supplier["capacity_mbd"] < required_mbd * 0.35:
            continue
        route = shortest_route(supplier["name"], destination, blocked)
        if not route:
            continue
        path, distance = route
        risk_penalty = 18 if "Bab el-Mandeb" in path else 4
        score = supplier["reliability"] - (supplier["price_index"] - 100) * 1.3 - distance / 750 - risk_penalty
        options.append({
            "supplier": supplier["name"], "region": supplier["region"], "available_mbd": supplier["capacity_mbd"],
            "route": path, "distance_nm": round(distance), "eta_days": round(distance / 336 + 2, 1),
            "landed_cost_delta_pct": round((supplier["price_index"] - 100) + distance / 1400, 1),
            "resilience_score": round(max(0, min(100, score))),
        })
    options.sort(key=lambda item: item["resilience_score"], reverse=True)
    coverage = min(required_mbd, sum(item["available_mbd"] * 0.45 for item in options[:2]))
    return {
        "blocked_nodes": blocked_nodes, "required_mbd": required_mbd, "recommended": options[:3],
        "recommended_mix": [{"supplier": item["supplier"], "allocation_mbd": round(min(required_mbd * 0.55, item["available_mbd"] * 0.45), 2)} for item in options[:2]],
        "coverage_pct": round(coverage / required_mbd * 100),
    }
