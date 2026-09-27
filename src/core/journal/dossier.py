"""
AEGIS / SENTRY
Trade Dossier & Psychological Timeline Engine

Implements the 360° Living Trade Record:
- Core trade execution metrics (MAE, MFE, Capture Efficiency)
- Pre-trade mindset & thesis capture
- Intra-trade real-time chronological event timeline (tags, notes, alerts)
- Process Adherence Audit & Objective Process Score (1-5★ decoupled from P&L)
- Dual-chart visual snapshots (Futures + Options)
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class TimelineEvent:
    timestamp: str              # HH:MM:SS
    event_type: str             # ENTRY_FILL, NOTE, TAG, TARGET_HIT, STOP_HIT, EXIT_FILL, FOL_WARNING
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TradeDossier:
    trade_id: str
    instrument: str                     # e.g., "NIFTY 23200 CE"
    strategy: str                       # e.g., "Deeppb5-15"
    setup: str
    entry_timestamp: str                # YYYY-MM-DD HH:MM:SS
    exit_timestamp: Optional[str] = None
    
    # Financials & Execution
    entry_price: float = 0.0
    exit_price: Optional[float] = None
    stop_loss_price: float = 0.0
    target_1_price: float = 0.0
    target_2_price: float = 0.0
    lots: int = 1
    qty: int = 65
    risk_rupees: float = 0.0
    realized_pnl: float = 0.0
    r_multiple: float = 0.0
    mae: Optional[float] = None
    mfe: Optional[float] = None
    capture_efficiency_pct: Optional[float] = None
    hold_duration_mins: Optional[float] = None

    # Pre-Trade Mindset & Preparation
    readiness_score: int = 0
    confidence_stars: int = 3
    pre_trade_checklist_done: bool = False
    thesis: str = ""
    premortem: str = ""
    pre_trade_emotion: str = "Calm"

    # Intra-Trade Psychological Timeline (Stream of consciousness)
    timeline_events: List[TimelineEvent] = field(default_factory=list)

    # Process Audit & Decoupled Score (1–5 Stars)
    pre_trade_compliant: bool = True
    entry_followup_evaluated: bool = True
    entry_bar_quality: str = "DECENT"       # STRONG, DECENT, POOR
    followup_bar_quality: str = "DECENT"    # STRONG, DECENT, POOR
    exit_discipline_type: str = "TARGET_HIT" # TARGET_HIT, STOP_HIT, AUTHORIZED_SCRATCH, CT_REVERSAL_EXIT, STAGNATION_EXIT, FOL_PREMATURE_EXIT
    process_score: int = 5                  # 1 to 5 Stars
    post_trade_lesson: str = ""

    # Visual Multi-Monitor Snapshots
    entry_futures_chart: Optional[str] = None
    entry_options_chart: Optional[str] = None
    exit_futures_chart: Optional[str] = None
    exit_options_chart: Optional[str] = None
    entry_composite: Optional[str] = None
    exit_composite: Optional[str] = None

    def add_event(self, event_type: str, content: str, timestamp: Optional[str] = None, **kwargs: Any) -> None:
        """Append an event to the chronological trade timeline."""
        ts = timestamp or datetime.now().strftime("%H:%M:%S")
        self.timeline_events.append(
            TimelineEvent(timestamp=ts, event_type=event_type, content=content, metadata=kwargs)
        )

    def calculate_process_score(self) -> int:
        """
        Calculates an objective process score (1 to 5 stars) decoupled from P&L.
        A disciplined loss gets 5 stars; an undisciplined win gets 1-2 stars.
        """
        score = 5

        # 1. Did trader exit on premature FOL panic?
        if self.exit_discipline_type == "FOL_PREMATURE_EXIT":
            score -= 3

        # 2. Was pre-trade checklist ignored?
        if not self.pre_trade_compliant or self.readiness_score < 80:
            score -= 2

        # 3. Were both entry & follow-up bars poor without scratching?
        if self.entry_bar_quality == "POOR" and self.followup_bar_quality == "POOR" and self.exit_discipline_type not in ["AUTHORIZED_SCRATCH", "STOP_HIT"]:
            score -= 1

        self.process_score = max(1, min(5, score))
        return self.process_score

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timeline_events"] = [e.to_dict() if isinstance(e, TimelineEvent) else e for e in self.timeline_events]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TradeDossier:
        raw_events = data.pop("timeline_events", [])
        events = [TimelineEvent(**e) if isinstance(e, dict) else e for e in raw_events]
        return cls(timeline_events=events, **data)
