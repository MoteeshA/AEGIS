from backend.services.procurement import recommend
from backend.services.reserve import optimize
from backend.services.risk import score_articles
from backend.services.scenario import simulate


def test_risk_is_bounded_and_explained():
    result = score_articles([{"title": "War escalation and Strait closure attack", "summary": "shipping disruption"}])
    assert 0 <= result["risk_score"] <= 100
    assert result["drivers"]


def test_blocked_hormuz_is_avoided():
    result = recommend("Saudi Arabia", "Rotterdam", ["Strait of Hormuz"], 1.2)
    assert result["recommended"]
    assert all("Strait of Hormuz" not in option["route"] for option in result["recommended"])


def test_scenario_and_reserve_are_feasible():
    scenario = simulate("strait_closure", 80, 30, 20.5)
    reserve = optimize(scenario["predicted_shortage_mbd"], 30, 92, 45)
    assert scenario["price_change_pct"] > 0
    assert reserve["reserve_after_release_million_bbl"] >= 45
