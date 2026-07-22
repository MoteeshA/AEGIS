"use client";

import { useMemo, useState } from "react";

const demo = {
  risk: { risk_score: 86, level: "critical", confidence: 0.89, drivers: [{ term: "escalation", mentions: 2 }, { term: "disruption", mentions: 2 }, { term: "war", mentions: 1 }] },
  scenario: { label: "Strait of Hormuz closure", predicted_shortage_mbd: 9.7, supply_impact_pct: 47.3, price_change_pct: 68.4, confidence_band: { low: 49.2, high: 87.6 } },
  procurement: {
    coverage_pct: 100,
    recommended: [
      { supplier: "Norway", region: "North Sea", route: ["Norway", "Rotterdam"], eta_days: 4.6, landed_cost_delta_pct: 6.6, resilience_score: 86 },
      { supplier: "United States", region: "Atlantic", route: ["United States", "Rotterdam"], eta_days: 13.6, landed_cost_delta_pct: 10.8, resilience_score: 74 },
      { supplier: "Brazil", region: "South Atlantic", route: ["Brazil", "Rotterdam"], eta_days: 17.2, landed_cost_delta_pct: 7.6, resilience_score: 72 },
    ],
  },
  reserve: { recommended_release_million_bbl: 47, daily_release_mbd: 1.57, reserve_after_release_million_bbl: 45, strategy: "Front-load 45% in week one, then taper as alternative cargoes arrive." },
};

const prices = [74.2, 75.1, 74.8, 76.4, 77.2, 78.1, 77.6, 79.4, 81, 82.7, 84.1, 86.4];
const news = [
  ["CRITICAL", "Naval tensions rise near Strait of Hormuz as tanker traffic slows", "8 min ago"],
  ["HIGH", "War-risk insurance premium increases for Gulf energy cargoes", "24 min ago"],
  ["WATCH", "Oman terminals remain operational under regional security alert", "41 min ago"],
];

export default function Home() {
  const [result, setResult] = useState(demo);
  const [severity, setSeverity] = useState(82);
  const [event, setEvent] = useState("strait_closure");
  const [running, setRunning] = useState(false);
  const [source, setSource] = useState("Local intelligence snapshot");
  const [chat, setChat] = useState("Ask: “What happens if the Strait of Hormuz closes?”");

  const chart = useMemo(() => prices.map((p, i) => `${(i / (prices.length - 1)) * 100},${90 - ((p - 72) / 16) * 70}`).join(" "), []);

  async function runSimulation() {
    setRunning(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/demo/run", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ severity }) });
      if (!response.ok) throw new Error("offline");
      setResult(await response.json());
      setSource("FastAPI decision engine • live local response");
    } catch {
      const factor = severity / 82;
      setResult({ ...demo, scenario: { ...demo.scenario, label: event === "war_escalation" ? "Regional war escalation" : "Strait of Hormuz closure", supply_impact_pct: +(demo.scenario.supply_impact_pct * factor).toFixed(1), price_change_pct: +(demo.scenario.price_change_pct * factor).toFixed(1), predicted_shortage_mbd: +(demo.scenario.predicted_shortage_mbd * factor).toFixed(1) } });
      setSource("Offline deterministic decision engine");
    } finally { setTimeout(() => setRunning(false), 450); }
  }

  function ask() {
    setChat(`A ${severity}% severity closure puts ~${result.scenario.predicted_shortage_mbd} mb/d at risk and may lift prices ${result.scenario.price_change_pct}%. Divert procurement to Norway and the US, while releasing ${result.reserve.daily_release_mbd} mb/d from reserves.`);
  }

  return (
    <main>
      <header>
        <div className="brand"><span className="brand-mark">AE</span><div><b>AEGIS</b><small>ENERGY RESILIENCE</small></div></div>
        <div className="system"><i /> SYSTEM ACTIVE <span>•</span> 12 SOURCES <span>•</span> UPDATED 2M AGO</div>
        <button className="icon-button" aria-label="Notifications">3</button>
      </header>

      <section className="hero">
        <div><p className="eyebrow">GLOBAL OPERATIONS / COMMAND CENTER</p><h1>Supply chain resilience,<br /><em>before disruption.</em></h1><p className="lede">AI-assisted intelligence turns geopolitical signals into procurement decisions in minutes, not days.</p></div>
        <div className="alert-card"><span className="pulse" /><div><small>ACTIVE THREAT</small><strong>Hormuz risk elevated</strong><p>Decision window: <b>18–36 hours</b></p></div><div className="score">{result.risk.risk_score}<small>/100</small></div></div>
      </section>

      <nav className="tabs"><button className="active">OVERVIEW</button><button>INTELLIGENCE</button><button>SCENARIOS</button><button>PROCUREMENT</button><button>RESERVES</button></nav>

      <section className="metrics">
        <Metric label="GLOBAL RISK INDEX" value={`${result.risk.risk_score}`} suffix="/100" change="↑ 18 pts / 24h" tone="danger" />
        <Metric label="SUPPLY AT RISK" value={`${result.scenario.predicted_shortage_mbd}`} suffix="mb/d" change={`${result.scenario.supply_impact_pct}% of monitored flow`} tone="amber" />
        <Metric label="PRICE EXPOSURE" value={`+${result.scenario.price_change_pct}`} suffix="%" change={`Band ${result.scenario.confidence_band?.low ?? 49}–${result.scenario.confidence_band?.high ?? 88}%`} tone="amber" />
        <Metric label="RESILIENCE COVERAGE" value={`${result.procurement.coverage_pct}`} suffix="%" change="Alternatives identified" tone="green" />
      </section>

      <section className="grid-main">
        <div className="panel map-panel">
          <PanelHead title="LIVE ROUTE EXPOSURE" meta="AIS + RISK OVERLAY" />
          <div className="map">
            <div className="gridlines" />
            <span className="land arabia">ARABIAN<br />PENINSULA</span><span className="land europe">EUROPE</span><span className="land africa">AFRICA</span>
            <div className="route primary" /><div className="route alternate" />
            <span className="node hormuz">!</span><span className="node suez" /><span className="node rotterdam" /><span className="node norway" />
            <div className="map-callout"><b>STRAIT OF HORMUZ</b><span>CRITICAL • 20.5 mb/d exposed</span></div>
            <div className="map-legend"><span><i className="red" /> Disrupted</span><span><i className="blue" /> Alternative</span><span><i className="white" /> Supplier</span></div>
          </div>
        </div>

        <div className="panel simulator">
          <PanelHead title="SCENARIO LAB" meta="DECISION MODEL" />
          <label>EVENT</label>
          <select value={event} onChange={e => setEvent(e.target.value)}><option value="strait_closure">Strait of Hormuz closure</option><option value="war_escalation">Regional war escalation</option><option value="sanctions">Expanded sanctions</option></select>
          <div className="slider-label"><label>SEVERITY</label><b>{severity}%</b></div>
          <input type="range" min="20" max="100" value={severity} onChange={e => setSeverity(+e.target.value)} />
          <div className="impact-grid"><div><small>SUPPLY IMPACT</small><b>−{result.scenario.supply_impact_pct}%</b></div><div><small>PRICE SHOCK</small><b>+{result.scenario.price_change_pct}%</b></div></div>
          <button className="run" onClick={runSimulation}>{running ? "SIMULATING…" : "RUN SIMULATION →"}</button>
          <p className="source">● {source}</p>
        </div>
      </section>

      <section className="grid-lower">
        <div className="panel intelligence"><PanelHead title="INTELLIGENCE FEED" meta="GDELT + MARITIME" />{news.map((item, i) => <article key={i}><span className={`tag t${i}`}>{item[0]}</span><div><b>{item[1]}</b><small>{item[2]} • NLP confidence {91 - i * 3}%</small></div></article>)}</div>
        <div className="panel"><PanelHead title="BRENT EXPOSURE" meta="12-MONTH SIGNAL" /><div className="price-head"><b>$86.40</b><span>+16.4%</span></div><svg className="line-chart" viewBox="0 0 100 100" preserveAspectRatio="none" aria-label="Oil price trend"><polyline points={chart} fill="none" stroke="currentColor" strokeWidth="2" vectorEffect="non-scaling-stroke" /></svg><div className="axis"><span>AUG</span><span>NOV</span><span>FEB</span><span>MAY</span><span>JUL</span></div></div>
        <div className="panel alternatives"><PanelHead title="RECOMMENDED ACTIONS" meta="RANKED BY RESILIENCE" />{result.procurement.recommended.map((route, i) => <article key={route.supplier}><span className="rank">0{i + 1}</span><div><b>{route.supplier} <small>{route.region}</small></b><p>{route.route.join(" → ")} • {route.eta_days} days</p></div><strong>{route.resilience_score}</strong></article>)}</div>
      </section>

      <section className="decision-strip"><div><small>STRATEGIC RESERVE PLAYBOOK</small><b>Release {result.reserve.recommended_release_million_bbl}M bbl, capped at {result.reserve.daily_release_mbd} mb/d</b><p>{result.reserve.strategy}</p></div><div className="reserve-stat"><span>AFTER ACTION</span><strong>{result.reserve.reserve_after_release_million_bbl}M</strong><small>barrels remain</small></div></section>

      <section className="chat"><div><span className="chat-mark">AI</span><p>{chat}</p></div><button onClick={ask}>ASK AEGIS ↗</button></section>
      <footer><span>AEGIS / PROTOTYPE 1.0</span><span>NO API KEYS • OFFLINE READY • EXPLAINABLE MODELS</span></footer>
    </main>
  );
}

function Metric({ label, value, suffix, change, tone }: { label: string; value: string; suffix: string; change: string; tone: string }) { return <div className={`metric ${tone}`}><small>{label}</small><div><strong>{value}</strong><span>{suffix}</span></div><p>{change}</p></div>; }
function PanelHead({ title, meta }: { title: string; meta: string }) { return <div className="panel-head"><b>{title}</b><span>{meta}</span></div>; }
