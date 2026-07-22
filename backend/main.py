from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .data.sources import data_hub
from .models import DemoRequest, ProcurementRequest, ReserveRequest, RiskRequest, ScenarioRequest
from .services.procurement import recommend
from .services.reserve import optimize
from .services.risk import score_articles
from .services.scenario import simulate

app = FastAPI(title="Aegis Energy Resilience API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], allow_methods=["*"], allow_headers=["*"])


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "offline-ready"}


@app.get("/api/data/snapshot")
def snapshot():
    return data_hub.snapshot()


@app.get("/api/news")
def news(live: bool = Query(default=False)):
    articles, source = data_hub.news(live)
    return {"articles": articles, "source": source}


@app.post("/api/risk/analyze")
def risk(request: RiskRequest):
    articles = [article.model_dump() for article in request.articles] or data_hub.snapshot()["articles"]
    return score_articles(articles)


@app.post("/api/scenarios/simulate")
def scenario(request: ScenarioRequest):
    return simulate(request.event, request.severity, request.duration_days, request.baseline_supply_mbd)


@app.post("/api/procurement/recommend")
def procurement(request: ProcurementRequest):
    return recommend(request.origin, request.destination, request.blocked_nodes, request.required_mbd)


@app.post("/api/reserves/optimize")
def reserves(request: ReserveRequest):
    return optimize(request.predicted_shortage_mbd, request.duration_days, request.reserve_available_million_bbl, request.minimum_reserve_million_bbl)


@app.post("/api/demo/run")
def demo(request: DemoRequest):
    articles = data_hub.snapshot()["articles"]
    risk_result = score_articles(articles)
    scenario_result = simulate("strait_closure", request.severity, 30, 20.5)
    procurement_result = recommend("Saudi Arabia", "Rotterdam", ["Strait of Hormuz"], 1.2)
    reserve_result = optimize(scenario_result["predicted_shortage_mbd"], 30, 92, 45)
    return {"risk": risk_result, "scenario": scenario_result, "procurement": procurement_result, "reserve": reserve_result, "articles": articles}
