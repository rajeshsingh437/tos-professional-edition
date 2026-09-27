"""
AEGIS Server
Build 0.2.002
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pathlib import Path

# Add project root and src to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from app.sentry_bridge import SentryApi

app = FastAPI(
    title="AEGIS Server",
    version="0.2.002",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_sentry_api = SentryApi()


@app.get("/")
def root():
    return {
        "name": "AEGIS Server",
        "version": "0.2.002",
        "status": "running",
    }


@app.get("/api/market-context")
def get_market_context():
    """
    Returns latest Market Context data from broker interface.
    """
    return _sentry_api.market_data_get_context()


@app.post("/api/decision/check-lockout")
def check_lockout(payload: dict):
    events = payload.get("events", [])
    active_flash = payload.get("active_flash")
    return _sentry_api.decision_check_lockout(events, active_flash)


@app.post("/api/decision/evaluate-regime")
def evaluate_regime(payload: dict):
    return _sentry_api.decision_evaluate_regime(
        nifty_lp=float(payload.get("nifty_lp", 23140.50)),
        nifty_chg=float(payload.get("nifty_chg", 0.0)),
        banknifty_chg=float(payload.get("banknifty_chg", 0.0)),
        gift_gap_pts=float(payload.get("gift_gap_pts", 0.0)),
        vix=float(payload.get("vix", 13.40)),
        crude_chg_pct=float(payload.get("crude_chg_pct", 0.0)),
        crude_price=float(payload.get("crude_price", 74.0)),
        usdinr_chg_pct=float(payload.get("usdinr_chg_pct", 0.0)),
        usdinr_rate=float(payload.get("usdinr_rate", 95.0)),
    )


@app.post("/api/decision/calculate-lots")
def calculate_lots(payload: dict):
    return _sentry_api.decision_calculate_lots(
        account_capital=float(payload.get("account_capital", 500000.0)),
        regime_risk_pct=float(payload.get("regime_risk_pct", 1.0)),
        psych_multiplier=float(payload.get("psych_multiplier", 1.0)),
        entry_px=float(payload.get("entry_px", 100.0)),
        stop_px=float(payload.get("stop_px", 80.0)),
        lot_size=int(payload.get("lot_size", 65)),
        daily_dd_remaining=float(payload.get("daily_dd_remaining", 15000.0)),
        loss_streak=int(payload.get("loss_streak", 0)),
    )


@app.post("/api/decision/generate-bracket")
def generate_bracket(payload: dict):
    return _sentry_api.decision_generate_bracket(
        entry=float(payload.get("entry", 100.0)),
        stop=float(payload.get("stop", 80.0)),
        total_lots=int(payload.get("total_lots", 1)),
        lot_size=int(payload.get("lot_size", 65)),
    )


@app.post("/api/decision/intercept-rogue")
def intercept_rogue(payload: dict):
    return _sentry_api.decision_intercept_rogue(
        broker_order_id=str(payload.get("broker_order_id", "")),
        approved_plan_ids=list(payload.get("approved_plan_ids", [])),
    )


@app.post("/api/decision/evaluate-exit-permission")
def evaluate_exit_permission(payload: dict):
    return _sentry_api.decision_evaluate_exit_permission(
        entry_bar_quality=str(payload.get("entry_bar_quality", "DECENT")),
        followup_bar_quality=str(payload.get("followup_bar_quality", "DECENT")),
        ct_setup_formed=bool(payload.get("ct_setup_formed", False)),
        legs_completed=int(payload.get("legs_completed", 0)),
        is_target_hit=bool(payload.get("is_target_hit", False)),
        is_stop_hit=bool(payload.get("is_stop_hit", False)),
    )


@app.post("/api/decision/check-trade-integrity")
def check_trade_integrity(payload: dict):
    return _sentry_api.decision_check_trade_integrity(
        setup_name=str(payload.get("setup_name", "")),
        is_preplanned_open_setup=bool(payload.get("is_preplanned_open_setup", False)),
        last_trade_was_loss=bool(payload.get("last_trade_was_loss", False)),
        minutes_since_last_stop=float(payload["minutes_since_last_stop"]) if payload.get("minutes_since_last_stop") is not None else None,
        is_preplanned_failure_setup=bool(payload.get("is_preplanned_failure_setup", False)),
        distance_to_ema=float(payload.get("distance_to_ema", 0.0)),
        max_allowed_ema_distance=float(payload.get("max_allowed_ema_distance", 35.0)),
        last_exit_was_fol=bool(payload.get("last_exit_was_fol", False)),
        minutes_since_last_exit=float(payload["minutes_since_last_exit"]) if payload.get("minutes_since_last_exit") is not None else None,
        is_same_instrument_as_last_exit=bool(payload.get("is_same_instrument_as_last_exit", False)),
    )





def main():
    print("=" * 55)
    print("AEGIS Server  Build 0.2.002")
    print("=" * 55)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8091,
    )


if __name__ == "__main__":
    main()
