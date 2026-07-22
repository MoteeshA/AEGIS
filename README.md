# Aegis — AI-Driven Energy Supply Chain Resilience

A complete, offline-ready hackathon prototype that converts geopolitical signals into disruption forecasts, alternative procurement plans, and strategic-reserve actions. No API keys are required.

## Architecture

```text
┌──────────────────────────── DATA INGESTION ─────────────────────────────┐
│ GDELT RSS       NOAA/USCG AIS       World Bank       UN Comtrade       │
│ geopolitical    vessel samples      oil prices       HS 2709 flows     │
└──────────────┬──────────────┬──────────────┬──────────────┬─────────────┘
               └──────────────┴──────┬───────┴──────────────┘
                                     ▼
                        ┌────────────────────────┐
                        │ DataHub / normalization │
                        │ cache + offline fallback│
                        └────────────┬───────────┘
                                     ▼
┌──────────────────────────────── AI / ML ────────────────────────────────┐
│ Explainable NLP risk scorer  │ Event profiles │ Confidence + drivers   │
└──────────────────────────────┬──────────────────────────────────────────┘
                               ▼
┌────────────────────────── DECISION ENGINE ──────────────────────────────┐
│ Scenario simulator │ Graph route search │ Supplier rank │ Reserve policy│
└──────────────────────────────┬──────────────────────────────────────────┘
                               ▼
                ┌──────────────────────────────┐
                │ FastAPI /api/* + OpenAPI docs │
                └──────────────┬───────────────┘
                               ▼
          ┌──────────────────────────────────────────────┐
          │ React command center                         │
          │ risk • map • scenarios • actions • AI Q&A    │
          └──────────────────────────────────────────────┘
```

The NLP module is intentionally explainable and local: a weighted threat lexicon, article-level evidence, saturation scoring, and confidence estimate. This is safer for a demo than pretending a hosted LLM is available. The procurement engine runs Dijkstra-style graph search with blocked chokepoints and ranks feasible suppliers using reliability, cost, distance, and route-risk penalties.

## Data strategy

| Signal | No-key source | Prototype behavior |
|---|---|---|
| Geopolitical news | [GDELT DOC 2.0 API / RSS](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/) | Optional `live=true`; 4-second timeout then local fallback |
| Shipping / AIS | [NOAA/USCG Marine Cadastre AIS](https://www.navcen.uscg.gov/ais-frequently-asked-questions) | Bundled realistic sample in the public dataset’s shape |
| Oil prices | [World Bank Commodity Markets “Pink Sheet”](https://www.worldbank.org/en/research/commodity-markets) | Bundled monthly Brent-like series; replaceable adapter |
| Supplier/trade flows | [UN Comtrade keyless preview API](https://uncomtrade.org/docs/un-comtrade-api/) | Bundled HS 2709 baseline; no-key preview-compatible |

The bundled snapshot makes judging deterministic. Network failure never blocks the product.

## Folder structure

```text
.
├── app/                       # React dashboard
│   ├── page.tsx               # command center + interactions
│   ├── globals.css            # responsive visual system
│   └── layout.tsx             # metadata and shell
├── backend/
│   ├── main.py                # FastAPI routes / demo orchestration
│   ├── models.py              # validated request schemas
│   ├── data/
│   │   ├── mock_data.py       # deterministic production-like snapshot
│   │   └── sources.py         # live/no-key adapters + fallback
│   └── services/
│       ├── risk.py            # explainable NLP classifier
│       ├── scenario.py        # disruption/price impact model
│       ├── procurement.py     # graph routing + supplier ranking
│       └── reserve.py         # reserve release optimizer
├── tests/test_engine.py       # decision-engine tests
├── requirements.txt
└── package.json
```

## Run locally

Requirements: Python 3.10+ and Node 22+.

Terminal 1 — API:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Terminal 2 — dashboard:

```bash
npm install
npm run dev
```

Open `http://localhost:3000`. Interactive API documentation is at `http://127.0.0.1:8000/docs`. If the API is not running, the dashboard still works with its deterministic local engine.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | health and offline-ready mode |
| `GET` | `/api/news?live=false` | news feed; opt into GDELT with `live=true` |
| `GET` | `/api/data/snapshot` | all demo data and provenance |
| `POST` | `/api/risk/analyze` | articles → 0–100 risk, confidence, drivers |
| `POST` | `/api/scenarios/simulate` | event/severity/duration → supply and price shock |
| `POST` | `/api/procurement/recommend` | blocked nodes → suppliers and routes |
| `POST` | `/api/reserves/optimize` | shortage → policy-floor-safe reserve release |
| `POST` | `/api/demo/run` | complete rising-tension demo in one call |

## Demo flow

1. Open the dashboard: a bundled feed reports rising Gulf tension and higher war-risk premiums.
2. The explainable risk agent scores the situation as critical and surfaces the strongest terms.
3. In **Scenario Lab**, choose “Strait of Hormuz closure,” adjust severity, and run the model.
4. The system estimates supply/price impact, blocks Hormuz in the route graph, and ranks Norway, the United States, and Brazil.
5. The reserve optimizer bridges the arrival window without crossing the 45M-barrel policy floor.
6. Click **Ask Aegis** for the natural-language executive answer.

## Sample requests and outputs

```bash
curl -s -X POST http://127.0.0.1:8000/api/scenarios/simulate \
  -H 'Content-Type: application/json' \
  -d '{"event":"strait_closure","severity":82,"duration_days":30,"baseline_supply_mbd":20.5}'
```

```json
{
  "event": "strait_closure",
  "predicted_shortage_mbd": 12.01,
  "supply_impact_pct": 58.6,
  "price_change_pct": 64.0,
  "confidence_band": {"low": 46.1, "high": 81.9}
}
```

```bash
curl -s -X POST http://127.0.0.1:8000/api/procurement/recommend \
  -H 'Content-Type: application/json' \
  -d '{"origin":"Saudi Arabia","destination":"Rotterdam","blocked_nodes":["Strait of Hormuz"],"required_mbd":1.2}'
```

The response includes ranked suppliers, safe path nodes, distance, ETA, landed-cost delta, resilience score, recommended allocation, and coverage.

## Model boundaries

All outputs are decision-support estimates, not trading advice. Production hardening would add authenticated feeds, streaming ingestion, probabilistic calibration against historical disruptions, vessel-level anomaly detection, contract constraints, emissions/capacity costs, audit logs, and human approval gates.
