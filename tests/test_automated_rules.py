"""
Unit tests for SENTRY Automated 'If A -> Then B' Decision Engine
"""

from datetime import time
import pytest

from src.core.automation.engine import (
    EventRadarGate,
    MarketContextGate,
    QuantDayTypeGate,
    PsychologyGate,
    DecisionEngineGate,
    RiskEngineGate,
    BracketOrderGenerator,
    RogueTradeInterceptor,
    TradeTelemetryCalculator,
    EdgeDriftSelfCorrection,
    FOLExitGuard,
    BadTradeGuard,
)


def test_gate1_budget_lockout():
    events = [{"tag": "budget", "title": "Union Budget", "rule": "NTD"}]
    res = EventRadarGate.check_lockout(events, time(10, 0))
    assert res.is_locked is True
    assert res.status_code == "MANDATORY_NTD"


def test_gate1_rbi_policy_lockout():
    events = [{"tag": "policy", "title": "RBI MPC", "rule": "NO_TRADE_TILL_11"}]
    # Before 11:00 AM
    res1 = EventRadarGate.check_lockout(events, time(10, 30))
    assert res1.is_locked is True
    assert res1.status_code == "LOCKOUT_TILL_11AM"

    # After 11:00 AM
    res2 = EventRadarGate.check_lockout(events, time(11, 15))
    assert res2.is_locked is False
    assert res2.status_code == "CLEAR"


def test_gate2_regime_evaluation():
    # Bullish confluence with normal VIX and stable crude
    eval_on = MarketContextGate.evaluate(
        nifty_lp=23200.0,
        nifty_chg=50.0,
        banknifty_chg=150.0,
        gift_gap_pts=45.0,
        vix=12.5,
        crude_chg_pct=-1.8,
        crude_price=70.0,
        usdinr_chg_pct=-0.2,
        usdinr_rate=94.50,
    )
    assert eval_on.tier == "RISK-ON"
    assert eval_on.sizing_multiplier == 1.0
    assert eval_on.day_bias == "BULLISH_CONFLUENCE"

    # Risk-off scenario (VIX spike, Crude spike, Falling INR)
    eval_off = MarketContextGate.evaluate(
        nifty_lp=23000.0,
        nifty_chg=-150.0,
        banknifty_chg=-450.0,
        gift_gap_pts=-80.0,
        vix=21.5,
        crude_chg_pct=3.5,
        crude_price=88.0,
        usdinr_chg_pct=0.45,
        usdinr_rate=96.10,
    )
    assert eval_off.tier == "RISK-OFF"
    assert eval_off.sizing_multiplier == 0.0


def test_gate3_quant_day_type():
    # Gap up with high CLV -> Trend Day
    dt, setups = QuantDayTypeGate.classify(
        open_px=23300.0,
        pd_high=23250.0,
        pd_low=23100.0,
        first_15min_clv=0.82
    )
    assert dt == "TREND_DAY"
    assert "Deeppb5-15" in setups
    assert "DT-DB-2LR" not in setups

    # Chop -> Range Day
    dt_tr, setups_tr = QuantDayTypeGate.classify(
        open_px=23200.0,
        pd_high=23250.0,
        pd_low=23100.0,
        first_15min_clv=0.50
    )
    assert dt_tr == "TR"
    assert "DT-DB-2LR" in setups_tr


def test_gate4_psychology():
    # C-game markers present
    res_c = PsychologyGate.check_state(
        c_game_markers_count=2,
        logged_tags=["FOL"],
        psych_score=48
    )
    assert res_c.status == "C_GAME_FLAGGED"
    assert res_c.max_risk_multiplier == 0.3
    assert res_c.cool_down_minutes == 15

    # A-game
    res_a = PsychologyGate.check_state(
        c_game_markers_count=0,
        logged_tags=["SOH"],
        psych_score=85
    )
    assert res_a.status == "A_GAME_CONFIRMED"
    assert res_a.max_risk_multiplier == 1.0


def test_gate5_decision_engine_readiness():
    allowed = ["1st Deeppb", "Deeppb5-15"]
    
    # Below 80% readiness
    ok1, reason1 = DecisionEngineGate.check_readiness("1st Deeppb", allowed, 75, True)
    assert ok1 is False
    assert "below 80%" in reason1

    # Disallowed setup for day type
    ok2, reason2 = DecisionEngineGate.check_readiness("DT-DB-2LR", allowed, 85, True)
    assert ok2 is False
    assert "locked for current Day-Type" in reason2

    # All pass
    ok3, _ = DecisionEngineGate.check_readiness("1st Deeppb", allowed, 85, True)
    assert ok3 is True


def test_gate6_risk_engine_sizing():
    # 3 losses streak -> Circuit breaker
    res_breaker = RiskEngineGate.calculate_lots(
        account_capital=500000.0,
        regime_risk_pct=1.0,
        psych_multiplier=1.0,
        entry_px=145.0,
        stop_px=105.0,
        lot_size=65,
        daily_dd_remaining=15000.0,
        loss_streak=3
    )
    assert res_breaker.allowed is False
    assert res_breaker.lots == 0
    assert "Loss-Streak Breaker" in res_breaker.reason

    # Normal sizing: Risk 0.75% of 500k = ₹3750. Per-lot risk = 40 * 65 = ₹2600.
    # Raw lots = floor(3750 / 2600) = 1 lot (65 units).
    res_normal = RiskEngineGate.calculate_lots(
        account_capital=500000.0,
        regime_risk_pct=0.75,
        psych_multiplier=1.0,
        entry_px=145.0,
        stop_px=105.0,
        lot_size=65,
        daily_dd_remaining=15000.0,
        loss_streak=0
    )
    assert res_normal.allowed is True
    assert res_normal.lots == 1
    assert res_normal.total_qty == 65
    assert res_normal.rupee_risk == 2600.0


def test_gate7_bracket_scale_out_generator():
    # 2 lots = 130 units. Stop width = 40 pts.
    # Target 1 (2R) = 145 + 80 = 225
    # Target 2 (4R) = 145 + 160 = 305
    bracket = BracketOrderGenerator.create_spec(
        entry=145.0,
        stop=105.0,
        total_lots=2,
        lot_size=65
    )
    assert bracket.target_1_price == 225.0
    assert bracket.target_1_qty == 65
    assert bracket.target_2_price == 305.0
    assert bracket.target_2_qty == 65
    assert bracket.stop_moves_to_be_on_t1 is True

    # Market order filled at 146.50 with 25 pts raw signal risk
    # 1. Protective SL with 7 pt options noise buffer -> Stop = 146.50 - 32 = 114.50
    # 2. Target 1 = min(2R, 20 pts) -> min(50, 20) = 20 pts -> 166.50
    # 3. Target 2 standard 45 pts -> 146.50 + 45 = 191.50
    bracket_mkt = BracketOrderGenerator.create_spec_from_fill(
        executed_price=146.50,
        risk_points=25.0,
        total_lots=2,
        lot_size=65,
        is_long=True,
        sl_buffer=7.0,
        t1_max_pts=20.0,
        t2_mode="standard_40_50",
        t2_custom_pts=45.0
    )
    assert bracket_mkt.entry_price == 146.50
    assert bracket_mkt.stop_loss_price == 114.50
    assert bracket_mkt.target_1_price == 166.50
    assert bracket_mkt.target_2_price == 191.50

    # Trend day big gain mode: Target 2 = min(4R, 100 pts) -> min(100, 100) = 100 pts -> 246.50
    bracket_big = BracketOrderGenerator.create_spec_from_fill(
        executed_price=146.50,
        risk_points=25.0,
        total_lots=2,
        lot_size=65,
        is_long=True,
        sl_buffer=5.0,
        t1_max_pts=20.0,
        t2_mode="big_gain_4r_100"
    )
    assert bracket_big.stop_loss_price == 116.50
    assert bracket_big.target_1_price == 166.50
    assert bracket_big.target_2_price == 246.50


def test_gate8_rogue_trade_interceptor():
    is_rogue, msg = RogueTradeInterceptor.intercept("FT_ORDER_9999", ["PLAN_1234"])
    assert is_rogue is True
    assert "UNPLANNED IMPULSE TRADE DETECTED" in msg

    is_valid, _ = RogueTradeInterceptor.intercept("PLAN_1234", ["PLAN_1234"])
    assert is_valid is False


def test_gate9_trade_telemetry_calculator():
    # Entry 145, Exit 225. High hit 240, low touched 128.
    metrics = TradeTelemetryCalculator.compute_metrics(
        entry_px=145.0,
        exit_px=225.0,
        tick_prices_during_trade=[145.0, 130.0, 128.0, 180.0, 240.0, 225.0],
        is_long=True
    )
    assert metrics["mae"] == 128.0
    assert metrics["mfe"] == 240.0
    # MFE gain = 240 - 145 = 95. Realized = 225 - 145 = 80.
    # Capture % = (80 / 95) * 100 = 84.2%
    assert metrics["capture_pct"] == 84.2


def test_gate10_edge_drift_monitor():
    recent = [-1.0, -1.0, 1.2, -1.0, -1.0, 0.5, -1.0, -1.0, -1.0, 1.0,
              -1.0, -1.0, -1.0, -1.0, 0.8, -1.0, -1.0, 1.1, -1.0, -1.0] # negative expectancy
    baseline = [1.5, 2.0, -1.0, 2.5, -1.0, 1.0, 2.0, -1.0, 1.5, 2.0] # positive baseline

    status, risk_mult = EdgeDriftSelfCorrection.evaluate_drift(recent, baseline)
    assert status == "DRIFT_REVERSED"
    assert risk_mult == 0.3 # Demoted to floor risk


def test_gate11_fol_exit_guard():
    # Scenario A: Scratch Rule (Both Entry Bar and Follow-up Bar are POOR) -> Allowed
    res_scratch = FOLExitGuard.evaluate_exit_permission(
        entry_bar_quality="POOR",
        followup_bar_quality="POOR"
    )
    assert res_scratch.allowed is True
    assert res_scratch.exit_type == "AUTHORIZED_SCRATCH"
    assert res_scratch.is_fol_violation is False

    # Scenario B: Premature FOL Exit (Entry bar was STRONG, no CT setup, stop not reached) -> BLOCKED
    res_fol = FOLExitGuard.evaluate_exit_permission(
        entry_bar_quality="STRONG",
        followup_bar_quality="DECENT",
        ct_setup_formed=False,
        legs_completed=1
    )
    assert res_fol.allowed is False
    assert res_fol.exit_type == "FOL_BLOCKED"
    assert res_fol.is_fol_violation is True

    # Scenario C: Counter-Trend setup formed on chart -> Allowed
    res_ct = FOLExitGuard.evaluate_exit_permission(
        entry_bar_quality="STRONG",
        followup_bar_quality="POOR",
        ct_setup_formed=True
    )
    assert res_ct.allowed is True
    assert res_ct.exit_type == "CT_REVERSAL_EXIT"
    assert res_ct.is_fol_violation is False

    # Scenario D: 2-3 Leg Stagnation without target reach -> Allowed
    res_stag = FOLExitGuard.evaluate_exit_permission(
        entry_bar_quality="STRONG",
        followup_bar_quality="STRONG",
        legs_completed=3
    )
    assert res_stag.allowed is True
    assert res_stag.exit_type == "STAGNATION_EXIT"
    assert res_stag.is_fol_violation is False


def test_gate12_bad_trade_guard():
    # 1. Opening Chaos: Entry at 09:20 without preplanned open setup -> BLOCKED
    res_open = BadTradeGuard.check_trade_integrity(
        current_time_ist=time(9, 20),
        setup_name="Impulse Open",
        is_preplanned_open_setup=False,
        last_trade_was_loss=False,
        minutes_since_last_stop=None,
        is_preplanned_failure_setup=False,
        distance_to_ema=10.0,
        max_allowed_ema_distance=35.0,
        last_exit_was_fol=False,
        minutes_since_last_exit=None
    )
    assert res_open.allowed is False
    assert res_open.status_code == "OPEN_CHAOS_LOCKED"

    # 2. Revenge Trade: Stop hit 6m ago without preplanned failure setup -> BLOCKED
    res_revenge = BadTradeGuard.check_trade_integrity(
        current_time_ist=time(10, 15),
        setup_name="Recovery CE",
        is_preplanned_open_setup=False,
        last_trade_was_loss=True,
        minutes_since_last_stop=6.0,
        is_preplanned_failure_setup=False,
        distance_to_ema=12.0,
        max_allowed_ema_distance=35.0,
        last_exit_was_fol=False,
        minutes_since_last_exit=None
    )
    assert res_revenge.allowed is False
    assert res_revenge.status_code == "REVENGE_RECOVERY_LOCKED"

    # 2b. Stop hit, but trade IS an explicitly preplanned failure setup -> ALLOWED
    res_failure = BadTradeGuard.check_trade_integrity(
        current_time_ist=time(10, 15),
        setup_name="Failure Rev. from 2nd Leg TCL",
        is_preplanned_open_setup=False,
        last_trade_was_loss=True,
        minutes_since_last_stop=6.0,
        is_preplanned_failure_setup=True,
        distance_to_ema=12.0,
        max_allowed_ema_distance=35.0,
        last_exit_was_fol=False,
        minutes_since_last_exit=None
    )
    assert res_failure.allowed is True
    assert res_failure.status_code == "INTEGRITY_VERIFIED"

    # 3. FOMO Extended Chasing: 65 pts from EMA vs 35 max allowed -> BLOCKED
    res_fomo = BadTradeGuard.check_trade_integrity(
        current_time_ist=time(11, 45),
        setup_name="BO-1Pb",
        is_preplanned_open_setup=False,
        last_trade_was_loss=False,
        minutes_since_last_stop=None,
        is_preplanned_failure_setup=False,
        distance_to_ema=65.0,
        max_allowed_ema_distance=35.0,
        last_exit_was_fol=False,
        minutes_since_last_exit=None
    )
    assert res_fomo.allowed is False
    assert res_fomo.status_code == "FOMO_EXTENSION_LOCKED"

    # 4. FOL Whipsaw Re-entry: Exited on FOL 4m ago on same contract -> BLOCKED
    res_whipsaw = BadTradeGuard.check_trade_integrity(
        current_time_ist=time(13, 10),
        setup_name="Re-entry CE",
        is_preplanned_open_setup=False,
        last_trade_was_loss=False,
        minutes_since_last_stop=None,
        is_preplanned_failure_setup=False,
        distance_to_ema=15.0,
        max_allowed_ema_distance=35.0,
        last_exit_was_fol=True,
        minutes_since_last_exit=4.0,
        is_same_instrument_as_last_exit=True
    )
    assert res_whipsaw.allowed is False
    assert res_whipsaw.status_code == "FOL_WHIPSAW_REENTRY_LOCKED"


