import pytest
from pathlib import Path
from src.core.screenshots.capture import ScreenshotCapture

def test_amibroker_export_resolution(tmp_path):
    cap = ScreenshotCapture(root=str(tmp_path))
    out_file = tmp_path / "test_chart.png"
    # Even if AmiBroker COM is offline or online, the call should not throw
    res = cap.export_amibroker_chart(out_file, document_name="NIFTY")
    assert isinstance(res, bool)

def test_dual_chart_phase_capture_pipeline(tmp_path):
    cap = ScreenshotCapture(root=str(tmp_path))
    phase_data = cap.capture_trade_phase(
        trade_id="UNIT_TEST_01",
        phase="ENTRY",
        futures_price=23190.0,
        options_price=140.0,
        instrument="NIFTY 23200 CE",
        timestamp_str="10:14:05"
    )
    assert "futures_chart" in phase_data
    assert "options_chart" in phase_data
    assert "composite" in phase_data
    assert Path(phase_data["composite"]).exists()
    assert Path(phase_data["composite"]).stat().st_size > 0
