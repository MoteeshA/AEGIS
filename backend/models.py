from typing import Literal

from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str
    summary: str = ""
    source: str = "demo"
    published_at: str = "2026-07-22T12:00:00Z"


class RiskRequest(BaseModel):
    articles: list[Article] = Field(default_factory=list)


class ScenarioRequest(BaseModel):
    event: Literal["strait_closure", "war_escalation", "sanctions", "port_disruption"]
    severity: int = Field(default=75, ge=0, le=100)
    duration_days: int = Field(default=30, ge=1, le=365)
    baseline_supply_mbd: float = Field(default=20.5, gt=0)


class ProcurementRequest(BaseModel):
    origin: str = "Saudi Arabia"
    destination: str = "Rotterdam"
    product: str = "Crude Oil"
    blocked_nodes: list[str] = Field(default_factory=lambda: ["Strait of Hormuz"])
    required_mbd: float = Field(default=1.2, gt=0)


class ReserveRequest(BaseModel):
    predicted_shortage_mbd: float = Field(default=2.4, ge=0)
    duration_days: int = Field(default=30, ge=1, le=365)
    reserve_available_million_bbl: float = Field(default=92, ge=0)
    minimum_reserve_million_bbl: float = Field(default=45, ge=0)


class DemoRequest(BaseModel):
    severity: int = Field(default=82, ge=0, le=100)
