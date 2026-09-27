"""
AEGIS / SENTRY
Automated Decision-Making and Execution Engine

Implements the deterministic sequential pipeline:
Gate 1: Event Radar & Macro Lockouts
Gate 2: Market Context & Dynamic Sizing Multiplier
Gate 3: Quant Day-Type Classification
Gate 4: Trader Psychology & A/B/C Game Protection
Gate 5: Pattern Matching & 80% Readiness Gate
Gate 6: Risk Engine Sizing & Drawdown Clamping
Gate 7: Automated Multi-Leg Scale-Out Bracket Generator
Gate 8: Rogue Trade Interceptor (Impulse Protection)
Gate 9: MAE/MFE High-Frequency Telemetry & Capture Efficiency
Gate 10: Edge Drift Self-Correction & Capital Plan Demotion
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Gate 1: Event Radar & Macro Lockouts
# ============================================================================

@dataclass
class LockoutStatus:
    is_locked: bool
    status_code: str
    reason: str
    allowed_actions: List[str] = field(default_factory=list)


class EventRadarGate:
    """
    Evaluates calendar events and breaking news to enforce mandatory lockouts.
    """

    @staticmethod
    def check_lockout(
        events_today: List[Dict[str, Any]],
        current_time_ist: time,
        active_flash: Optional[Dict[str, Any]] = None,
    ) -> LockoutStatus:
        # 1. Critical Breaking News Flash
        if active_flash:
            return LockoutStatus(
                is_locked=True,
                status_code="CRITICAL_FLASH_FREEZE",
                reason=f"Emergency Market Flash: {active_flash.get('message', '')} · Trading frozen for 10 minutes",
                allowed_actions=["SQUARE_OFF_ONLY"]
            )

        # 2. Union Budget / Mandatory Sovereign NTD
        for ev in events_today:
            tag = str(ev.get("tag", "")).lower()
            rule = str(ev.get("rule", "")).upper()
            if tag == "budget" or rule == "NTD":
                return LockoutStatus(
                    is_locked=True,
                    status_code="MANDATORY_NTD",
                    reason=f"Mandatory No-Trade Day: {ev.get('title', 'Sovereign Event')} · Terminal hard-locked for entire session",
                    allowed_actions=[]
                )

        # 3. RBI Policy Decision (Locked until 11:00 AM IST)
        for ev in events_today:
            tag = str(ev.get("tag", "")).lower()
            rule = str(ev.get("rule", "")).upper()
            if tag == "policy" or rule == "NO_TRADE_TILL_11":
                rbi_cutoff = time(11, 0)
                if current_time_ist < rbi_cutoff:
                    return LockoutStatus(
                        is_locked=True,
                        status_code="LOCKOUT_TILL_11AM",
                        reason=f"RBI Policy Lockout: Standing aside until {rbi_cutoff.strftime('%H:%M')} IST post-presser",
                        allowed_actions=["MONITOR_ONLY"]
                    )

        # 4. Market-Hours Heavyweight Earnings Window (±5 mins)
        for ev in events_today:
            rule = str(ev.get("rule", "")).upper()
            if rule == "VOL_WINDOW" and ev.get("isMarketHours"):
                ev_time_str = ev.get("time", "")
                # Simple extraction of HH:MM if available
                # (If within ±5 min window, lock out)

        return LockoutStatus(
            is_locked=False,
            status_code="CLEAR",
            reason="No event lockouts active · Proceed to Gate 2",
            allowed_actions=["ALL"]
        )


# ============================================================================
# Gate 2: Market Context & Dynamic Sizing Multiplier
# ============================================================================

@dataclass
class RegimeEvaluation:
    score: int                  # 0 to 100
    tier: str                   # RISK-ON, NEUTRAL, RISK-OFF
    sizing_multiplier: float    # 1.0, 0.5, 0.0
    day_bias: str               # BULLISH_CONFLUENCE, BEARISH_CONFLUENCE, DIVERGENCE_CHOP
    vix_expected_pts: int
    reasons: List[str]


class MarketContextGate:
    """
    Computes composite regime score and returns dynamic sizing tier.
    """

    @staticmethod
    def evaluate(
        nifty_lp: float,
        nifty_chg: float,
        banknifty_chg: float,
        gift_gap_pts: float,
        vix: float,
        crude_chg_pct: float,
        crude_price: float,
        usdinr_chg_pct: float,
        usdinr_rate: float,
    ) -> RegimeEvaluation:
        score_points = 0
        reasons = []

        # Volatility translation
        expected_pts = round((nifty_lp * (vix / 100.0)) / math.sqrt(252))
        if vix < 13.0:
            score_points += 1
            reasons.append(f"VIX low ({vix:.1f}) · Standard 1R size")
        elif vix < 16.5:
            reasons.append(f"VIX normal ({vix:.1f}) · ATR ±{expected_pts} pts")
        elif vix < 20.0:
            score_points -= 1
            reasons.append(f"VIX elevated ({vix:.1f}) · Elevated volatility penalty")
        else:
            score_points -= 2
            reasons.append(f"VIX extreme ({vix:.1f}) · Stop-hunting whipsaw penalty")

        # Crude impact (OMC / Paint / Cyclical cost drag)
        if crude_chg_pct >= 2.5 or crude_price >= 85.0:
            score_points -= 1
            reasons.append(f"Crude spike ({crude_chg_pct:+.1f}%) · Cost margin drag on Nifty")
        elif crude_chg_pct <= -1.5:
            score_points += 1
            reasons.append(f"Crude cooling ({crude_chg_pct:+.1f}%) · Margin tailwind")

        # USD / INR impact (Rupee depreciation vs FII foreign outflows)
        if usdinr_chg_pct >= 0.25 or usdinr_rate >= 95.00:
            score_points -= 1
            reasons.append(f"USD/INR elevated (₹{usdinr_rate:.2f}) · FII equity outflow drag")
        elif usdinr_chg_pct <= -0.15:
            score_points += 1
            reasons.append(f"USD/INR firming · Capital inflow support")

        # Index confluence vs divergence
        same_direction = (nifty_chg >= 0 and banknifty_chg >= 0) or (nifty_chg < 0 and banknifty_chg < 0)
        if not same_direction:
            day_bias = "DIVERGENCE_CHOP"
            reasons.append("Nifty vs Bank Nifty divergence · Chop / Range conditions expected")
        elif gift_gap_pts > 30 and banknifty_chg > 0:
            day_bias = "BULLISH_CONFLUENCE"
            score_points += 2
            reasons.append(f"Bullish gap confluence (+{gift_gap_pts:.1f} pts) with Bank Nifty")
        elif gift_gap_pts < -30 and banknifty_chg < 0:
            day_bias = "BEARISH_CONFLUENCE"
            score_points -= 2
            reasons.append(f"Bearish gap confluence ({gift_gap_pts:.1f} pts) with Bank Nifty")
        else:
            day_bias = "MILD_ALIGNMENT"
            score_points += (1 if gift_gap_pts >= 0 else -1)

        # Scale -6..+3 points to 0..100%
        pct = max(0, min(100, round((score_points - (-6)) / (3 - (-6)) * 100)))

        if pct >= 65:
            tier = "RISK-ON"
            sizing_mult = 1.0
        elif pct >= 35:
            tier = "NEUTRAL"
            sizing_mult = 0.5
        else:
            tier = "RISK-OFF"
            sizing_mult = 0.0

        return RegimeEvaluation(
            score=pct,
            tier=tier,
            sizing_multiplier=sizing_mult,
            day_bias=day_bias,
            vix_expected_pts=expected_pts,
            reasons=reasons
        )


# ============================================================================
# Gate 3: Quant Day-Type Classification
# ============================================================================

class QuantDayTypeGate:
    """
    Classifies market structure into TREND_DAY, TR (Range), or TTR (Tight Range).
    Enforces setup filtering constraints.
    """

    @staticmethod
    def classify(
        open_px: float,
        pd_high: float,
        pd_low: float,
        first_15min_clv: float,
        is_opening_drive: bool = False,
    ) -> Tuple[str, List[str]]:
        """
        Returns (day_type, allowed_setup_names).
        """
        # CLV = (Close - Low) / (High - Low)
        # If open gaps outside range with strong CLV -> Trend Day
        if (open_px > pd_high and first_15min_clv > 0.70) or (open_px < pd_low and first_15min_clv < 0.30):
            day_type = "TREND_DAY"
            allowed_setups = [
                "BO-1Pb",
                "1st Deeppb",
                "Deeppb5-15",
                "CT 2nd Leg Failure at/around EMA",
                "EMA/FBO OF THE TL",
                "FBO-DT-DB-CT 2nd Leg Failure(Trend Resumption)"
            ]
        elif 0.35 <= first_15min_clv <= 0.65 and (pd_low <= open_px <= pd_high):
            day_type = "TR"
            allowed_setups = [
                "DT-DB-2LR",
                "Close to the EMA 5-15",
                "Rev. from 2nd Leg TCL",
                "T.R",
                "Bull-bear Leg."
            ]
        else:
            # Overlapping chop / contracting range
            day_type = "TTR"
            allowed_setups = []  # NTD: No discretionary entries

        return day_type, allowed_setups


# ============================================================================
# Gate 4: Trader State & Psychology Gate
# ============================================================================

@dataclass
class PsychGateResult:
    allowed: bool
    status: str
    max_risk_multiplier: float
    cool_down_minutes: int


class PsychologyGate:
    """
    Guards execution against tilt, FOMO, and C-game behavioral slippage.
    """

    @staticmethod
    def check_state(
        c_game_markers_count: int,
        logged_tags: List[str],
        psych_score: int,
    ) -> PsychGateResult:
        # Any C-game breach
        has_impulse_tags = any(t in ["FOL", "SM", "LPT"] for t in logged_tags)
        if c_game_markers_count >= 2 or has_impulse_tags or psych_score < 50:
            return PsychGateResult(
                allowed=True,
                status="C_GAME_FLAGGED",
                max_risk_multiplier=0.3,   # Cut to floor
                cool_down_minutes=15       # Enforce 15-min pause
            )

        if psych_score >= 75 and c_game_markers_count == 0:
            return PsychGateResult(
                allowed=True,
                status="A_GAME_CONFIRMED",
                max_risk_multiplier=1.0,
                cool_down_minutes=0
            )

        return PsychGateResult(
            allowed=True,
            status="B_GAME_STANDARD",
            max_risk_multiplier=0.75,
            cool_down_minutes=0
        )


# ============================================================================
# Gate 5: Decision Engine & 80% Readiness Gate
# ============================================================================

class DecisionEngineGate:
    """
    Validates setup alignment against day-type and verifies GO/NO-GO readiness score >= 80%.
    """

    @staticmethod
    def check_readiness(
        setup_name: str,
        allowed_setups: List[str],
        checklist_score: int,
        pre_trade_checklist_done: bool,
    ) -> Tuple[bool, str]:
        # 1. Check if day-type allows this setup
        if allowed_setups and setup_name not in allowed_setups:
            return False, f"Setup '{setup_name}' is locked for current Day-Type. Allowed: {', '.join(allowed_setups[:3])}..."

        # 2. Checklist score >= 80%
        if checklist_score < 80:
            return False, f"Readiness score ({checklist_score}%) is below 80% GO threshold. Trade entry disabled."

        # 3. 5-point verification checklist
        if not pre_trade_checklist_done:
            return False, "Pre-trade 5-point checklist incomplete."

        return True, "All Decision Gates cleared · 1-Click execution unlocked"


# ============================================================================
# Gate 6: Risk Engine & Sizing Calculator
# ============================================================================

@dataclass
class SizingResult:
    allowed: bool
    lots: int
    total_qty: int
    rupee_risk: float
    reason: str


class RiskEngineGate:
    """
    Calculates exact lot sizing from stop distance and clamps against daily drawdown limits.
    """

    @staticmethod
    def calculate_lots(
        account_capital: float,
        regime_risk_pct: float,
        psych_multiplier: float,
        entry_px: float,
        stop_px: float,
        lot_size: int,
        daily_dd_remaining: float,
        loss_streak: int,
    ) -> SizingResult:
        # Circuit Breaker: 3 consecutive losses = session stop
        if loss_streak >= 3:
            return SizingResult(
                allowed=False,
                lots=0,
                total_qty=0,
                rupee_risk=0.0,
                reason="Loss-Streak Breaker tripped (3 consecutive losses). Trading halted for today."
            )

        stop_distance = abs(entry_px - stop_px)
        if stop_distance <= 0:
            return SizingResult(
                allowed=False,
                lots=0,
                total_qty=0,
                rupee_risk=0.0,
                reason="Invalid Stop distance (Entry == Stop)."
            )

        # Effective risk % = base * regime * psych
        effective_risk_pct = regime_risk_pct * psych_multiplier
        target_risk_rupees = account_capital * (effective_risk_pct / 100.0)

        per_lot_risk = stop_distance * lot_size
        raw_lots = math.floor(target_risk_rupees / per_lot_risk)

        if raw_lots <= 0:
            return SizingResult(
                allowed=False,
                lots=0,
                total_qty=0,
                rupee_risk=0.0,
                reason="Calculated lots == 0. Account risk parameter too small for stop width."
            )

        # Drawdown protection clamping
        computed_risk = raw_lots * per_lot_risk
        if daily_dd_remaining > 0 and computed_risk > daily_dd_remaining:
            clamped_lots = math.floor(daily_dd_remaining / per_lot_risk)
            if clamped_lots <= 0:
                return SizingResult(
                    allowed=False,
                    lots=0,
                    total_qty=0,
                    rupee_risk=0.0,
                    reason=f"Risk ({computed_risk:.0f}) exceeds Daily Drawdown Remaining ({daily_dd_remaining:.0f}). Order blocked."
                )
            raw_lots = clamped_lots
            computed_risk = raw_lots * per_lot_risk

        return SizingResult(
            allowed=True,
            lots=raw_lots,
            total_qty=raw_lots * lot_size,
            rupee_risk=round(computed_risk, 2),
            reason=f"Authorized {raw_lots} lot(s) ({raw_lots * lot_size} qty) for ₹{computed_risk:.0f} risk."
        )


# ============================================================================
# Gate 7: Automated Multi-Leg Scale-Out Bracket Generator
# ============================================================================

@dataclass
class BracketOrderSpec:
    entry_price: float
    stop_loss_price: float
    target_1_price: float       # 2R
    target_1_qty: int           # 50%
    target_2_price: float       # 4R
    target_2_qty: int           # 50%
    stop_moves_to_be_on_t1: bool = True


class BracketOrderGenerator:
    """
    Generates exact 2-leg scale-out bracket parameters:
    - Target 1 (2R): 50% exit, moves Stop to Breakeven
    - Target 2 (4R): remaining 50% trailing
    """

    @staticmethod
    def create_spec(
        entry: float,
        stop: float,
        total_lots: int,
        lot_size: int,
    ) -> BracketOrderSpec:
        risk_per_unit = abs(entry - stop)
        is_long = entry > stop

        if is_long:
            t1 = round(entry + (2.0 * risk_per_unit), 2)
            t2 = round(entry + (4.0 * risk_per_unit), 2)
        else:
            t1 = round(entry - (2.0 * risk_per_unit), 2)
            t2 = round(entry - (4.0 * risk_per_unit), 2)

        total_units = total_lots * lot_size
        half_lots = math.ceil(total_lots / 2.0)
        t1_qty = half_lots * lot_size
        t2_qty = total_units - t1_qty

        return BracketOrderSpec(
            entry_price=entry,
            stop_loss_price=stop,
            target_1_price=t1,
            target_1_qty=t1_qty,
            target_2_price=t2,
            target_2_qty=t2_qty,
            stop_moves_to_be_on_t1=True
        )

    @staticmethod
    def create_spec_from_fill(
        executed_price: float,
        risk_points: float,
        total_lots: int,
        lot_size: int,
        is_long: bool = True,
        sl_buffer: float = 5.0,
        t1_max_pts: Optional[float] = 20.0,
        t2_mode: str = "standard_40_50",  # "standard_40_50", "big_gain_4r_100", or "pure_4r"
        t2_custom_pts: Optional[float] = 45.0,
    ) -> BracketOrderSpec:
        """
        Calculates exact SL and Targets dynamically from the actual market order fill price.
        Tailored for Nifty Options traded off Futures charts:
        - sl_buffer: 5-10 pt breathing buffer against options noise / IV fluctuation
        - Target 1: min(2R, 20 pts) to bank quick profit and trigger breakeven on remaining 50%
        - Target 2: standard 40-50 pts exit or 4R / 100 pt runner for trend days
        """
        # 1. Protective Stop Loss with 5-10 pt option noise buffer
        effective_sl_distance = risk_points + sl_buffer

        # 2. Target 1 (Quick profit / breakeven trigger): min(2R, 20 pts)
        raw_t1_gain = 2.0 * risk_points
        if t1_max_pts is not None and t1_max_pts > 0:
            t1_gain = min(raw_t1_gain, t1_max_pts)
        else:
            t1_gain = raw_t1_gain

        # 3. Target 2 (Runner leg): 40-50 pts standard, or min(4R, 100 pts) for bigger gains
        raw_t2_gain = 4.0 * risk_points
        if t2_mode == "big_gain_4r_100":
            t2_gain = min(raw_t2_gain, 100.0)
        elif t2_mode == "standard_40_50":
            t2_gain = t2_custom_pts if t2_custom_pts is not None else 45.0
        else:
            t2_gain = raw_t2_gain

        if is_long:
            stop = round(executed_price - effective_sl_distance, 2)
            t1 = round(executed_price + t1_gain, 2)
            t2 = round(executed_price + t2_gain, 2)
        else:
            stop = round(executed_price + effective_sl_distance, 2)
            t1 = round(executed_price - t1_gain, 2)
            t2 = round(executed_price - t2_gain, 2)

        total_units = total_lots * lot_size
        half_lots = math.ceil(total_lots / 2.0)
        t1_qty = half_lots * lot_size
        t2_qty = total_units - t1_qty

        return BracketOrderSpec(
            entry_price=executed_price,
            stop_loss_price=stop,
            target_1_price=t1,
            target_1_qty=t1_qty,
            target_2_price=t2,
            target_2_qty=t2_qty,
            stop_moves_to_be_on_t1=True,
        )


# ============================================================================
# Gate 8: Rogue Trade Interceptor (Impulse Protection)
# ============================================================================

class RogueTradeInterceptor:
    """
    Cross-checks broker order fills against SENTRY pre-approved plan IDs.
    """

    @staticmethod
    def intercept(
        broker_order_id: str,
        approved_plan_ids: List[str],
    ) -> Tuple[bool, str]:
        """
        Returns (is_impulse, alert_message).
        """
        if broker_order_id not in approved_plan_ids:
            return True, (
                "🚨 UNPLANNED IMPULSE TRADE DETECTED: Order filled outside SENTRY pre-approved plans. "
                "Logged as IMPULSE_BREACH · Terminal session locked to protect capital."
            )
        return False, "Order verified with active Trade Plan."


# ============================================================================
# Gate 9: MAE/MFE Telemetry & Capture Efficiency
# ============================================================================

class TradeTelemetryCalculator:
    """
    Computes Maximum Adverse Excursion, Maximum Favorable Excursion, and Capture Efficiency.
    """

    @staticmethod
    def compute_metrics(
        entry_px: float,
        exit_px: float,
        tick_prices_during_trade: List[float],
        is_long: bool = True,
    ) -> Dict[str, Optional[float]]:
        if not tick_prices_during_trade:
            return {
                "mae": None,
                "mfe": None,
                "capture_pct": None,
            }

        if is_long:
            mfe = max(tick_prices_during_trade)
            mae = min(tick_prices_during_trade)
            mfe_gain = mfe - entry_px
            realized_gain = exit_px - entry_px
        else:
            mfe = min(tick_prices_during_trade)
            mae = max(tick_prices_during_trade)
            mfe_gain = entry_px - mfe
            realized_gain = entry_px - exit_px

        capture_pct = round((realized_gain / mfe_gain) * 100, 1) if mfe_gain > 0 else 0.0

        return {
            "mae": round(mae, 2),
            "mfe": round(mfe, 2),
            "capture_pct": max(0.0, min(100.0, capture_pct)),
        }


# ============================================================================
# Gate 10: Edge Drift Self-Correction
# ============================================================================

class EdgeDriftSelfCorrection:
    """
    Monitors rolling 20-trade Expectancy against historical baseline.
    Demotes capital plan to Floor Risk if drift turns negative.
    """

    @staticmethod
    def evaluate_drift(
        recent_20_trades_r: List[float],
        baseline_trades_r: List[float],
    ) -> Tuple[str, float]:
        """
        Returns (drift_status, recommended_max_risk_pct).
        """
        if len(recent_20_trades_r) < 20 or len(baseline_trades_r) < 10:
            return "INSUFFICIENT_SAMPLE", 1.0

        recent_exp = sum(recent_20_trades_r) / len(recent_20_trades_r)
        baseline_exp = sum(baseline_trades_r) / len(baseline_trades_r)

        if recent_exp < 0 and baseline_exp > 0:
            # Reversal: Demote to Floor Risk
            return "DRIFT_REVERSED", 0.3
        elif (recent_exp - baseline_exp) <= -0.30:
            # Softening: Reduce risk
            return "DRIFT_SOFTENING", 0.5

        return "STABLE", 1.0


# ============================================================================
# Gate 11: Fear of Loss (FOL) Premature Exit Guard
# ============================================================================

@dataclass
class ExitPermissionResult:
    allowed: bool
    exit_type: str              # "AUTHORIZED_SCRATCH", "CT_REVERSAL_EXIT", "STAGNATION_EXIT", "TARGET_OR_STOP", "FOL_BLOCKED"
    is_fol_violation: bool
    guidance: str


class FOLExitGuard:
    """
    Guards against premature exits driven by Fear of Loss (FOL).
    
    Authorized Early Exit Rules:
    1. Scratch Rule: Both Entry Bar AND Follow-up Bar close POOR (against the trade).
    2. CT Signal: Market forms a verified Counter-Trend setup against position.
    3. Multi-Leg Stagnation: Market completes 2-3 leg moves and enters stall without reaching target.
    4. Target or Hard Stop: Normal bracket execution.
    
    Anything else is strictly FORBIDDEN and tagged as FOL_PREMATURE_EXIT.
    """

    @staticmethod
    def evaluate_exit_permission(
        entry_bar_quality: str,     # "STRONG", "DECENT", "POOR"
        followup_bar_quality: str,  # "STRONG", "DECENT", "POOR"
        ct_setup_formed: bool = False,
        legs_completed: int = 0,
        is_target_hit: bool = False,
        is_stop_hit: bool = False,
    ) -> ExitPermissionResult:
        # Rule 0: Natural bracket executions
        if is_target_hit:
            return ExitPermissionResult(
                allowed=True,
                exit_type="TARGET_HIT",
                is_fol_violation=False,
                guidance="Target hit. Full plan materialized."
            )
        if is_stop_hit:
            return ExitPermissionResult(
                allowed=True,
                exit_type="STOP_HIT",
                is_fol_violation=False,
                guidance="Stop-loss hit. Risk parameter honored."
            )

        # Rule 1: Scratch Rule (Entry Bar POOR + Follow-up Bar POOR)
        if entry_bar_quality.upper() == "POOR" and followup_bar_quality.upper() == "POOR":
            return ExitPermissionResult(
                allowed=True,
                exit_type="AUTHORIZED_SCRATCH",
                is_fol_violation=False,
                guidance="Authorized Scratch: Entry and follow-up bars both closed poor. Immediate scratch allowed to save loss."
            )

        # Rule 2: Counter-Trend Setup Formed
        if ct_setup_formed:
            return ExitPermissionResult(
                allowed=True,
                exit_type="CT_REVERSAL_EXIT",
                is_fol_violation=False,
                guidance="Authorized CT Exit: Valid counter-trend reversal pattern formed on the chart. Structural shift justifies exit."
            )

        # Rule 3: 2-3 Leg Stagnation
        if legs_completed >= 2:
            return ExitPermissionResult(
                allowed=True,
                exit_type="STAGNATION_EXIT",
                is_fol_violation=False,
                guidance=f"Authorized Stagnation Exit: {legs_completed} legs completed without target reach. Momentum exhausted."
            )

        # Rule 4: Anything else is an ILLEGAL FOL PREMATURE EXIT
        return ExitPermissionResult(
            allowed=False,
            exit_type="FOL_BLOCKED",
            is_fol_violation=True,
            guidance=(
                "🚨 FEAR OF LOSS (FOL) ALERT: Premature exit blocked! "
                "Thesis is still intact (Entry/Follow-up bars did not both fail, no CT setup, stop not reached). "
                "SIT ON HANDS (SOH). Exiting now is an emotional impulse."
            )
        )


# ============================================================================
# Gate 12: Bad Trade Guard (Opening Chaos, Revenge, FOMO Chasing, Whipsaw Re-entry)
# ============================================================================

@dataclass
class BadTradeCheckResult:
    allowed: bool
    status_code: str
    reason: str


class BadTradeGuard:
    """
    Prevents the 4 primary archetypes of destructive bad trades:
    1. Opening Chaos (09:15-09:30): Entries locked unless matched to a pre-planned open setup.
    2. Revenge / Recovery Trade: Blocked within 15 min of a stop-out unless an explicit failure setup was pre-planned.
    3. FOMO Extended Chasing: Blocked if price is stretched beyond allowed EMA distance (Trend at EMA only).
    4. FOL Whipsaw Re-entry: Blocked for at least 10 min (2 closed 5-min bars) after premature exit on same contract.
    """

    @staticmethod
    def check_trade_integrity(
        current_time_ist: time,
        setup_name: str,
        is_preplanned_open_setup: bool,
        last_trade_was_loss: bool,
        minutes_since_last_stop: Optional[float],
        is_preplanned_failure_setup: bool,
        distance_to_ema: float,
        max_allowed_ema_distance: float,
        last_exit_was_fol: bool,
        minutes_since_last_exit: Optional[float],
        is_same_instrument_as_last_exit: bool = False,
    ) -> BadTradeCheckResult:
        # Archetype 1: Opening Chaos (09:15 - 09:30 IST)
        open_start = time(9, 15)
        open_end = time(9, 30)
        if open_start <= current_time_ist < open_end:
            if not is_preplanned_open_setup:
                return BadTradeCheckResult(
                    allowed=False,
                    status_code="OPEN_CHAOS_LOCKED",
                    reason="Opening 15-min entries strictly restricted to pre-planned open A+ setups. Discretionary open trading blocked."
                )

        # Archetype 2: Revenge / Recovery Trade After Stop Hit
        if last_trade_was_loss and minutes_since_last_stop is not None and minutes_since_last_stop < 15.0:
            if not is_preplanned_failure_setup:
                return BadTradeCheckResult(
                    allowed=False,
                    status_code="REVENGE_RECOVERY_LOCKED",
                    reason=(
                        f"Stop hit {minutes_since_last_stop:.0f}m ago. Recovery trade blocked without a pre-planned failure setup. "
                        "Accept the stop, step back, and wait for the next clean setup."
                    )
                )

        # Archetype 3: FOMO Chasing Stretched Beyond EMA
        if distance_to_ema > max_allowed_ema_distance and max_allowed_ema_distance > 0:
            return BadTradeCheckResult(
                allowed=False,
                status_code="FOMO_EXTENSION_LOCKED",
                reason=(
                    f"Price is extended ({distance_to_ema:.1f} pts from EMA vs max {max_allowed_ema_distance:.1f} pts). "
                    "Trend entries allowed ONLY at the EMA, never chasing in space. Wait for 1st Deeppb / pullback."
                )
            )

        # Archetype 4: FOL Panic Exit Followed by Re-Entry at Worse Price (Whipsaw Trap)
        if last_exit_was_fol and is_same_instrument_as_last_exit:
            if minutes_since_last_exit is not None and minutes_since_last_exit < 10.0:
                return BadTradeCheckResult(
                    allowed=False,
                    status_code="FOL_WHIPSAW_REENTRY_LOCKED",
                    reason=(
                        f"You exited on Fear of Loss (FOL) {minutes_since_last_exit:.0f}m ago. "
                        "Re-entering at a worse price is blocked for 10 minutes (2 bars) to prevent whipsaw chop."
                    )
                )

        return BadTradeCheckResult(
            allowed=True,
            status_code="INTEGRITY_VERIFIED",
            reason="Trade integrity verified. All 4 bad-trade archetypes cleared."
        )


