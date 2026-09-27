"""
Unit tests for SENTRY Trade Dossier, Psychological Timeline, and Dual-Chart Screenshots
"""

from pathlib import Path
import pytest

from src.core.journal.dossier import TradeDossier, TimelineEvent
from src.core.screenshots.capture import ScreenshotCapture


def test_trade_dossier_lifecycle_and_timeline():
    dossier = TradeDossier(
        trade_id="TR_1001",
        instrument="NIFTY 23200 CE",
        strategy="Deeppb5-15",
        setup="1st Deeppb",
        entry_timestamp="2026-09-26 10:14:05",
        entry_price=140.0,
        stop_loss_price=118.0,
        target_1_price=160.0,
        target_2_price=185.0,
        lots=2,
        qty=130,
        risk_rupees=2860.0,
        readiness_score=85,
        confidence_stars=4,
        pre_trade_checklist_done=True,
        thesis="Breakout continuation from 15 EMA after morning trend spike",
        premortem="Might drag into TTR if Bank Nifty fails to cross 55600",
        pre_trade_emotion="Calm"
    )

    # 1. Append real-time timeline events
    dossier.add_event("ENTRY_FILL", "Filled 2 lots @ ₹140.00", timestamp="10:14:05")
    dossier.add_event("NOTE", "Strong follow-up bar closed. Speed confirmed.", timestamp="10:18:20")
    dossier.add_event("TAG", "FOL urge noticed on 3 pt pullback - SOH enforced", timestamp="10:22:15", tag="FOL")
    dossier.add_event("TARGET_HIT", "Target 1 hit @ ₹160.00. 1 lot closed. SL to BE.", timestamp="10:25:40")
    dossier.add_event("EXIT_FILL", "Target 2 hit @ ₹185.00. Position flat.", timestamp="10:32:10")

    assert len(dossier.timeline_events) == 5
    assert dossier.timeline_events[0].event_type == "ENTRY_FILL"
    assert dossier.timeline_events[2].content.startswith("FOL urge")

    # 2. Check serialization
    d = dossier.to_dict()
    assert d["trade_id"] == "TR_1001"
    assert len(d["timeline_events"]) == 5

    restored = TradeDossier.from_dict(d)
    assert restored.trade_id == "TR_1001"
    assert len(restored.timeline_events) == 5
    assert restored.timeline_events[3].event_type == "TARGET_HIT"


def test_process_score_calculation_decoupled_from_pnl():
    # Trade A: Lost ₹2,000, but followed every rule perfectly -> 5 Stars
    dossier_good_loss = TradeDossier(
        trade_id="TR_1002",
        instrument="NIFTY 23200 CE",
        strategy="Deeppb5-15",
        setup="1st Deeppb",
        entry_timestamp="2026-09-26 11:00:00",
        realized_pnl=-2000.0,
        pre_trade_compliant=True,
        readiness_score=85,
        entry_bar_quality="POOR",
        followup_bar_quality="POOR",
        exit_discipline_type="AUTHORIZED_SCRATCH"
    )
    score_a = dossier_good_loss.calculate_process_score()
    assert score_a == 5 # Full 5 Stars despite loss!

    # Trade B: Made ₹5,000, but panicked out on FOL prematurely -> Penalized score
    dossier_bad_win = TradeDossier(
        trade_id="TR_1003",
        instrument="NIFTY 23200 CE",
        strategy="Deeppb5-15",
        setup="1st Deeppb",
        entry_timestamp="2026-09-26 11:30:00",
        realized_pnl=5000.0,
        pre_trade_compliant=True,
        readiness_score=85,
        entry_bar_quality="STRONG",
        followup_bar_quality="STRONG",
        exit_discipline_type="FOL_PREMATURE_EXIT"
    )
    score_b = dossier_bad_win.calculate_process_score()
    assert score_b == 2 # Only 2 Stars despite profitable trade!


def test_dual_chart_screenshot_capture_and_compositor(tmp_path):
    capture = ScreenshotCapture(root=str(tmp_path / "screenshots"))

    # Test full capture phase pipeline
    phase_data = capture.capture_trade_phase(
        trade_id="TR_999",
        phase="ENTRY",
        futures_price=23210.50,
        options_price=142.00,
        instrument="NIFTY 23200 CE",
        timestamp_str="10:14:05"
    )

    assert "futures_chart" in phase_data
    assert "options_chart" in phase_data
    assert "composite" in phase_data

    fut_file = Path(phase_data["futures_chart"])
    opt_file = Path(phase_data["options_chart"])
    comp_file = Path(phase_data["composite"])

    assert fut_file.exists()
    assert opt_file.exists()
    assert comp_file.exists()

    # Verify composite image dimensions (side-by-side)
    from PIL import Image
    with Image.open(comp_file) as img:
        assert img.width > 1500 # 800 * 2 + padding
        assert img.height > 500
