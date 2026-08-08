"""
AEGIS

Screenshot Capture Service
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    import pyautogui
except ImportError:
    pyautogui = None


class ScreenshotCapture:
    """
    Handles screenshot capture for AEGIS.

    Screenshots are stored under:

        screenshots/YYYY-MM-DD/
    """

    def __init__(
        self,
        root: str = "screenshots",
    ) -> None:

        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def capture(
        self,
        prefix: str = "trade",
    ) -> Path:

        if pyautogui is None:

            raise RuntimeError(
                "pyautogui is not installed."
            )

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        folder = self.root / today

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            f"{prefix}_"
            f"{datetime.now():%H%M%S}.png"
        )

        path = folder / filename

        image = pyautogui.screenshot()

        image.save(path)

        return path

    def latest(self) -> Path | None:

        files = sorted(
            self.root.rglob("*.png")
        )

        if not files:

            return None

        return files[-1]
