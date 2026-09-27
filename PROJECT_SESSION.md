# ============================================================

# TOS PROFESSIONAL EDITION

# PROJECT SESSION

# ============================================================

## Project Information

Project Name:
Trading Operating System (TOS) Professional Edition

Repository:
https://github.com/rajeshsingh437/tos-professional-edition

Technology Stack:

- Python
- PySide6
- SQLite (Planned)
- pandas
- pyqtgraph

Branch:
main

---

# Current Status

Current Build:
0.2.002

Current Phase:
Application Framework

Application Status:
✅ Running Successfully

Current Architecture:
Python Desktop Application

---

# Completed Files

app/
✔ application.py
✔ main.py

ui/
✔ dashboard.py
✔ header.py
✔ main_window.py
✔ sidebar.py
✔ theme.py

---

# Pending Files

□ PROJECT_MASTER.md
□ WORK_LOG.md
□ start.ps1
□ run.ps1
□ build.ps1
□ commit.ps1
□ clean.ps1

---

# Current Decisions

✔ Python Desktop only

✔ SENTRY is reference-only

✔ One complete file per response

✔ Replace entire file only

✔ Verify after every file

✔ Git commit only after stable build

✔ Branch:
main

✔ Modular architecture

---

# Current Folder Structure

TOS Professional Edition/

app/

ui/

docs/

---

# Next Build Target

Build 0.2.002

Objectives:

1. Create project documentation
2. Build application framework
3. Implement QStackedWidget navigation
4. Create page architecture
5. Create reusable UI components

---

# Next File

PROJECT_MASTER.md

---

# Session Start Checklist

□ Open PROJECT_SESSION.md

□ Verify project folder

□ Activate .venv

□ Run application

□ Continue from "Next File"

---

# Session End Checklist

□ Application runs

□ Git Commit

□ Git Push

□ Update CHANGELOG.md

□ Update PROJECT_SESSION.md

---

# Notes

Old React/Vite project still exists.

Repository cleanup will be done after Build 0.2.002.

---

Build 0.2.003
SENTRY Market Context, Flattrade Broker Data Sync & Institutional Event Radar

## Latest Development Progress — 2026-09-26

- **Market Context Engine**:
  - Reordered the 7 market cards to trader hierarchy: `GIFT NIFTY` (1) → `NIFTY 50` (2) → `BANK NIFTY` (3) → `SENSEX` (4) → `INDIA VIX` (5) → `CRUDE` (6) → `USD / INR` (7).
  - Wired live GIFT Nifty implied gap calculation against Nifty 50 spot.
  - Implemented Nifty-First India VIX translation (`Expected Swing ±185 pts · Position Sizing`).
  - Added dynamic macro risk calculations for Elevated Crude (`CRUDE SPIKE` > +2.5% / OMC & Paint drag) and Falling INR (`INR FALLING BIG` > +0.25% / FII outflow drag).
  - Combined index gap confluence with macro threats in unified alignment warning strip (`Caution: Crude spike & INR elevated`).

- **Broker Interface Integration (Flattrade)**:
  - Replaced third-party web scrapers with direct Flattrade broker interface pipelines.
  - Enhanced `app/sentry_bridge.py` with REST `GetQuotes` fallback and `market_data_get_context()`.
  - Added CORS-enabled FastAPI endpoint `/api/market-context` in `server/main.py` (port 8091) for browser tabs.
  - Synced baseline / closing levels with active AmiBroker terminal charts: Nifty `23,140.50`, Bank Nifty `55,580.40`, USD/INR `₹95.82`.
  - Updated both `D:\Projects\sentry-trading-os\dashboard\index.html` and `d:\Project-Python\AEGIS\migration\dashboard\index.html`.

- **Event Radar & Institutional Calendar**:
  - Automated event countdowns (RBI MPC `IN 13 DAYS`, TCS Q2 `IN 16 DAYS`).
  - Emergency breaking flash banner with dismiss control.
  - Interactive simulator buttons for RBI policy, Budget NTD, and Macro spikes.

- **Quant Engine Inter-Project Link**:
  - Installed `Nifty_Quant_Architect` (`D:\Project-Python\Nifty_Quant_Architect`) as an active editable package (`pip install -e`) inside AEGIS's `.venv`.
  - Enables direct, zero-copy imports of 5-min bar classification (`BarClassifier`, `compute_clv`, `determine_vol_regime`) into AEGIS guardrails and decision engines.

---

Build 0.2.005
SENTRY Real-Time AmiBroker COM Capture, Full UTF-8 Dashboard Restoration & Execution Workstation HUD

## Latest Development Progress — 2026-09-26

- **Live AmiBroker OLE/COM Dual-Chart Pipeline Verified (`src/core/screenshots/capture.py`)**:
  - Live verified against running AmiBroker 6.20.1 (PID 14872) using Windows COM dispatch.
  - Implemented absolute path resolution for Windows COM `ActiveWindow.ExportImage` and dynamic tab switching across `NIFTY-I` and option tabs via `Documents(i).Activate()`.
  - Added Windows native Segoe UI TrueType typography rendering for high-contrast annotation badges:
    - ▲ Green Entry Badge: `▲ ENTRY: ₹142.50 @ 10:14:05 (NIFTY 23200 CE)`
    - ▼ Red Exit Badge: `▼ EXIT: ₹185.00 @ 10:32:10 (NIFTY 23200 CE)`
  - Successfully generated and verified live dual-chart composite files in `screenshots/2026-09-26/`.

- **Comprehensive Dashboard UTF-8 Mojibake Restoration**:
  - Successfully resolved all 670+ corrupted encoding instances across both repositories (`AEGIS/migration/dashboard/index.html` and `sentry-trading-os/dashboard/index.html`).
  - Restored all Rupee symbols (`₹`), em-dashes (`—`), en-dashes (`–`), comparison operators (`≥`), ellipses (`…`), process star ratings (`★ ★ ★ ☆ ☆`), delete trashcans (`🗑️`), memos (`📝`), moon indicators (`🌙`), and printers (`🖨️`).
  - Modernized sidebar navigation items with clean icons: `▣ Home Dashboard`, `◈ Decision Engine`, `🛡️ Risk Engine`, `📓 Trade Journal`, `📋 Checklists`, `📈 Analytics`, `🧠 Psychology`, `⚖ Discipline Protocol`, `🌐 Market Events`, `📊 Reports`, `⚙ Settings & Rulebook`.
  - Fixed CSS mask vendorPrefix warnings: 0 warnings in VS Code.

- **Modular SENTRY Execution Workstation (`migration/dashboard/sentry_execution_workstation.js`)**:
  - **Single-Click Execution Gate**: "⚡ AUTHORIZE MARKET ENTRY & SPAWN BRACKET" panel with 5-10 pt noise buffer, T1 at min(2R, 20 pts) with auto-BE shift, and T2 runner.
  - **Active Trade HUD**: 5-Min Candle Quality Monitor (Entry Bar & Follow-up Bar toggles `STRONG`, `DECENT`, `POOR`) with automated Scratch Trade Alert banner.
  - **Fear of Loss (FOL) Guard**: Intercepts premature emotional exit clicks; requires deliberate confirmation or technical validation (scratch/CT/stagnation/targets).
  - **Psychological Timeline Logger**: 1-click pills (`CALM`, `IN_THE_ZONE`, `FOL`, `FOMO`, `ANXIOUS`, `SM`) + quick note bar directly stamping into Trade Dossier.
  - **15-Minute Post-Stop Cool-Down Countdown**: Auto-arms on loss or FOL breach to block revenge trading.

- **Automated Test Suite**:
  - Full suite verified: **18 tests passed in 4.40s** (100% pass rate) via `tests/test_automated_rules.py`, `tests/test_trade_dossier.py`, and `tests/test_amibroker_live_capture.py`.

---

# Next Session Roadmap (Monday Test Run with 1 Lot)

1. **Flattrade Real-Order Live Hookup**:
   - Connect `handleAuthorizeMarketEntry` in `sentry_execution_workstation.js` directly to Flattrade REST API (`place_order`) to fire the real 1-lot Market Order on Nifty Option and auto-place the bracket on fill.
2. **Pre-Market Readiness Checklist**:
   - Run pre-market verification on Monday morning: Flattrade token refresh, AmiBroker NIFTY-I chart active on Laptop, Option chart on Extended Monitor.
3. **Live 1-Lot Pilot Test Run**:
   - Execute first live 1-lot trade using the SENTRY Execution Gate, verify automatic AmiBroker dual-chart capture, live bar quality tracking, and clean journal logging.

