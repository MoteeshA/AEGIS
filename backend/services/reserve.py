def optimize(shortage_mbd: float, duration_days: int, available: float, minimum: float) -> dict:
    usable = max(0, available - minimum)
    total_shortage = shortage_mbd * duration_days
    # Reserve bridges the first shock, capped to preserve the policy floor.
    release = min(usable, total_shortage * 0.38)
    daily = min(shortage_mbd * 0.55, release / max(duration_days, 1))
    days_covered = release / shortage_mbd if shortage_mbd else 0
    return {
        "recommended_release_million_bbl": round(release, 1),
        "daily_release_mbd": round(daily, 2),
        "days_of_shortage_covered": round(days_covered, 1),
        "reserve_after_release_million_bbl": round(available - release, 1),
        "policy_floor_respected": available - release >= minimum,
        "uncovered_shortage_million_bbl": round(max(0, total_shortage - release), 1),
        "strategy": "Front-load 45% in week one, then taper as alternative cargoes arrive.",
    }
