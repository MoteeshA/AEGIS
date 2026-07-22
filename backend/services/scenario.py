EVENTS = {
    "strait_closure": {"flow_at_risk": 20.5, "elasticity": 1.15, "label": "Strait of Hormuz closure"},
    "war_escalation": {"flow_at_risk": 8.0, "elasticity": 0.82, "label": "Regional war escalation"},
    "sanctions": {"flow_at_risk": 4.2, "elasticity": 0.68, "label": "Expanded producer sanctions"},
    "port_disruption": {"flow_at_risk": 2.5, "elasticity": 0.44, "label": "Major export port disruption"},
}


def simulate(event: str, severity: int, duration_days: int, baseline_supply_mbd: float) -> dict:
    profile = EVENTS[event]
    severity_factor = severity / 100
    duration_factor = min(1.45, 0.55 + duration_days / 75)
    gross = profile["flow_at_risk"] * severity_factor
    substitution = min(gross * 0.42, 4.8)
    net_shortage = max(0, gross - substitution)
    supply_impact_pct = min(65, net_shortage / baseline_supply_mbd * 100)
    price_change_pct = min(85, supply_impact_pct * profile["elasticity"] * duration_factor)
    return {
        "event": event,
        "label": profile["label"],
        "severity": severity,
        "duration_days": duration_days,
        "gross_flow_at_risk_mbd": round(gross, 2),
        "substitutable_mbd": round(substitution, 2),
        "predicted_shortage_mbd": round(net_shortage, 2),
        "supply_impact_pct": round(supply_impact_pct, 1),
        "price_change_pct": round(price_change_pct, 1),
        "confidence_band": {"low": round(price_change_pct * 0.72, 1), "high": round(price_change_pct * 1.28, 1)},
        "assumptions": ["Static short-run demand", "Partial supplier substitution", "No second-order infrastructure damage"],
    }
