"""
AEGIS / SENTRY
Multi-Monitor & Dual-Chart Screenshot Capture Service

Capabilities:
1. AmiBroker OLE/COM Export (`Broker.Application -> ActiveWindow.ExportImage`)
2. Auto-Annotation: Overlays Entry (▲ Green) and Exit (▼ Red) marker badges with price & timestamp
3. Side-by-Side Dual Chart Compositor: Combines Nifty Futures (Laptop) + Option Contract (Extended Monitor)
4. Offline / Fallback Canvas Generation for test suites and disconnect resilience
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

try:
    import win32com.client
except ImportError:
    win32com = None

try:
    import pyautogui
except ImportError:
    pyautogui = None


class ScreenshotCapture:
    """
    Handles multi-monitor chart capture, annotation, and composite generation.
    """

    def __init__(self, root: str = "screenshots") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _get_daily_folder(self) -> Path:
        today = datetime.now().strftime("%Y-%m-%d")
        folder = self.root / today
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def export_amibroker_chart(
        self,
        output_path: Path,
        document_name: Optional[str] = None,
        width: int = 1280,
        height: int = 720,
    ) -> bool:
        """
        Attempts to capture chart directly from AmiBroker via Windows OLE/COM.
        Supports selecting a specific document/tab (e.g. Futures vs Options).
        """
        if win32com is None:
            return False

        try:
            ab = win32com.client.Dispatch("Broker.Application")
            target_path = output_path.resolve()
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # If a specific document is requested, find and activate it
            prev_doc = None
            if document_name and hasattr(ab, "Documents") and ab.Documents.Count > 0:
                try:
                    prev_doc = ab.ActiveDocument
                    for i in range(ab.Documents.Count):
                        doc = ab.Documents(i)
                        if document_name.lower() in doc.Name.lower():
                            doc.Activate()
                            break
                except Exception as doc_err:
                    print(f"[ScreenshotCapture] Doc activation note: {doc_err}")

            if hasattr(ab, "ActiveWindow") and hasattr(ab.ActiveWindow, "ExportImage"):
                res = ab.ActiveWindow.ExportImage(str(target_path), width, height)
                
                # Restore previous document if switched
                if prev_doc:
                    try:
                        prev_doc.Activate()
                    except Exception:
                        pass
                        
                return target_path.exists()
        except Exception as e:
            print(f"[ScreenshotCapture] AmiBroker COM export unavailable: {e}")

        return False

    def create_fallback_chart(
        self,
        output_path: Path,
        chart_title: str = "NIFTY FUTURES 5-MIN",
        width: int = 1280,
        height: int = 720,
    ) -> Path:
        """
        Generates a synthetic dark-theme chart canvas when broker/AmiBroker is offline.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (width, height), color=(17, 21, 29))
        draw = ImageDraw.Draw(img)

        # Draw grid lines
        for y in range(80, height - 40, 80):
            draw.line([(40, y), (width - 40, y)], fill=(35, 42, 56), width=1)
        for x in range(80, width - 40, 120):
            draw.line([(x, 80), (x, height - 40)], fill=(35, 42, 56), width=1)

        # Title bar
        draw.rectangle([(0, 0), (width, 45)], fill=(22, 27, 37))
        draw.text((20, 14), chart_title, fill=(231, 234, 241))
        draw.text((width - 180, 14), datetime.now().strftime("%Y-%m-%d %H:%M"), fill=(139, 147, 167))

        img.save(output_path)
        return output_path

    @staticmethod
    def _get_font(size: int = 14, bold: bool = False):
        font_paths = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    return ImageFont.truetype(fp, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    def annotate_chart_marker(
        self,
        image_path: Path,
        marker_type: str = "ENTRY",   # "ENTRY" or "EXIT"
        price: float = 140.0,
        timestamp_str: str = "10:14:05",
        instrument: str = "NIFTY 23200 CE",
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Draws high-contrast Entry (▲ Green) or Exit (▼ Red) marker badges directly on the chart.
        """
        target = output_path or image_path
        if not image_path.exists():
            self.create_fallback_chart(image_path, chart_title=f"{instrument} CHART")

        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        w, h = img.size

        is_entry = marker_type.upper() == "ENTRY"
        badge_color = (47, 217, 139) if is_entry else (240, 82, 95)   # Green vs Red
        text_color = (10, 13, 18)
        arrow_sym = "▲" if is_entry else "▼"
        label = f"{arrow_sym} {marker_type.upper()}: ₹{price:.2f} @ {timestamp_str} ({instrument})"

        font = self._get_font(15, bold=True)
        # Position marker badge at bottom-right or center-right
        box_w, box_h = 420, 38
        box_x = w - box_w - 30
        box_y = h - box_h - 30

        # Background badge & border
        draw.rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], fill=badge_color)
        draw.rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], outline=(255, 255, 255), width=2)
        draw.text((box_x + 16, box_y + 8), label, fill=text_color, font=font)

        img.save(target)
        return target

    def create_side_by_side_composite(
        self,
        futures_img_path: Path,
        options_img_path: Path,
        output_path: Path,
        composite_title: str = "SENTRY DUAL CHART SNAPSHOT",
    ) -> Path:
        """
        Combines Futures Chart (Left) + Options Chart (Right) into a unified side-by-side composite.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not futures_img_path.exists():
            self.create_fallback_chart(futures_img_path, "NIFTY FUTURES (LAPTOP SCREEN)")
        if not options_img_path.exists():
            self.create_fallback_chart(options_img_path, "NIFTY OPTIONS 5-MIN (EXTENDED MONITOR)")

        img_left = Image.open(futures_img_path).convert("RGB")
        img_right = Image.open(options_img_path).convert("RGB")

        # Standardize sub-chart dimensions
        chart_w, chart_h = 800, 480
        img_left_resized = img_left.resize((chart_w, chart_h), Image.Resampling.LANCZOS)
        img_right_resized = img_right.resize((chart_w, chart_h), Image.Resampling.LANCZOS)

        header_h = 44
        composite_w = (chart_w * 2) + 16
        composite_h = chart_h + header_h + 16

        composite = Image.new("RGB", (composite_w, composite_h), color=(10, 13, 18))
        draw = ImageDraw.Draw(composite)

        # Header bar
        draw.rectangle([(0, 0), (composite_w, header_h)], fill=(22, 27, 37))
        draw.text((20, 14), composite_title, fill=(203, 168, 105)) # Gold brand
        draw.text((composite_w - 240, 14), datetime.now().strftime("%Y-%m-%d %H:%M:%S IST"), fill=(139, 147, 167))

        # Paste left & right charts
        composite.paste(img_left_resized, (8, header_h + 8))
        composite.paste(img_right_resized, (chart_w + 12, header_h + 8))

        # Labels on charts
        draw.rectangle([(16, header_h + 16), (220, header_h + 40)], fill=(0, 0, 0))
        draw.text((24, header_h + 20), "FUTURES CONTEXT (LEFT)", fill=(76, 141, 255))

        draw.rectangle([(chart_w + 20, header_h + 16), (chart_w + 230, header_h + 40)], fill=(0, 0, 0))
        draw.text((chart_w + 28, header_h + 20), "OPTION CONTRACT (RIGHT)", fill=(47, 217, 139))

        composite.save(output_path)
        return output_path

    def capture_trade_phase(
        self,
        trade_id: str,
        phase: str = "ENTRY",       # "ENTRY" or "EXIT"
        futures_price: float = 23200.0,
        options_price: float = 140.0,
        instrument: str = "NIFTY 23200 CE",
        timestamp_str: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Executes complete dual-chart capture pipeline for a trade phase:
        - Captures/exports Futures and Options charts
        - Annotates marker arrows (▲ Entry / ▼ Exit)
        - Generates side-by-side composite
        """
        folder = self._get_daily_folder()
        ts = timestamp_str or datetime.now().strftime("%H:%M:%S")
        ts_clean = ts.replace(":", "")

        fut_path = folder / f"trade_{trade_id}_{phase}_futures_{ts_clean}.png"
        opt_path = folder / f"trade_{trade_id}_{phase}_options_{ts_clean}.png"
        comp_path = folder / f"trade_{trade_id}_{phase}_composite_{ts_clean}.png"

        # 1. Capture Futures (Laptop Screen or NIFTY Document)
        if not self.export_amibroker_chart(fut_path, document_name="NIFTY"):
            self.create_fallback_chart(fut_path, f"NIFTY FUTURES · {phase}")

        # 2. Capture Options (Extended Monitor or Option Document)
        if not self.export_amibroker_chart(opt_path, document_name=instrument):
            self.create_fallback_chart(opt_path, f"{instrument} · {phase}")

        # 3. Annotate markers
        self.annotate_chart_marker(
            image_path=fut_path,
            marker_type=phase,
            price=futures_price,
            timestamp_str=ts,
            instrument="NIFTY FUT"
        )
        self.annotate_chart_marker(
            image_path=opt_path,
            marker_type=phase,
            price=options_price,
            timestamp_str=ts,
            instrument=instrument
        )

        # 4. Generate Composite
        title = f"SENTRY TRADE #{trade_id} · {phase.upper()} SNAPSHOT"
        self.create_side_by_side_composite(fut_path, opt_path, comp_path, title)

        return {
            "futures_chart": str(fut_path),
            "options_chart": str(opt_path),
            "composite": str(comp_path),
        }
