# SENTRY UI Production Blueprint & Implementation Plan
**Status**: 100% Locked & Approved by Trader  
**Date**: September 26, 2026  
**Target Environment**: AEGIS · SENTRY Trading Operating System (PyWebView + Flattrade + AmiBroker + Telegram + SQLite)

---

## Executive Summary
SENTRY was originally prototyped as an offline manual journal. This revision transforms it into a **live, real-time, broker-integrated institutional trading cockpit**.

---

## 1. Tab 1: Home Dashboard (`view-home`) — LOCKED
* **Top Bar**:
  * Title & Version: `SENTRY · Trading Operating System`
  * Broker Status Pill: `● FLATTRADE · LIVE` (pulsing green if active / amber if closed).
  * Session Phase Pill: `Pre-Market` | `Session Open` | `After Hours` | `Closed · Weekend`.
  * Live Precision IST Clock (`HH:MM:SS IST · Day DD Mon`).
* **Top KPI Strip (8 Live Metrics)**:
  1. `Readiness` (0–100 score + GO/CAUTION/NO-GO badge)
  2. `Today's P&L` (Live ₹ and R: `+₹4,250 (+1.85R)` / `0 trades today`)
  3. `Win Rate` (% and count)
  4. `Expectancy` (R per trade)
  5. `Profit Factor` (Gross wins / gross losses)
  6. `Avg R` (Overall edge multiple)
  7. `Current Drawdown` (Live peak-to-trough in R)
  8. `Psychology Score` (0–100 composite)
* **Market Context Panel (Nifty-First Hierarchy)**:
  * 7 Live Cards: `GIFT Nifty` (with gap pts), `Nifty 50 Spot`, `Bank Nifty Spot`, `Sensex`, `India VIX` (with intraday ATR swing in pts), `Crude (Brent)` (with OMC/Inflation tag), `USD/INR` (with FII flow tag).
  * Global Cues & Index Alignment Strip (S&P, NQ, DAX, Nikkei + Bullish/Bearish Confluence verdict e.g. `[INDEX DIVERGENCE (CHOP)]`).
* **Event Radar & Breaking Pulse Bar**:
  * Single-line emergency flash banner (`🚨 BREAKING FLASH` if triggered).
  * Upcoming high-impact event pills with countdowns (`TODAY`, `TOMORROW`) and automated guardrail tags (`NO TRADE TILL 11:00 AM`, `5-MIN VOL WINDOW`, `MANDATORY NTD`).
* **Row 1 (Two Pillars: External vs Internal)**:
  * **Left: Pre-Market Regime & Key Levels (External)**:
    * Dynamic Regime Arc Dial (0–100) from VIX, Crude, INR, and Events.
    * Posture Note: `Risk-On (Full Size)`, `Neutral (Trade Smaller)`, `Lockout / NTD`.
    * Key Levels: Today's Open vs PDC, Gap Pts, PDH, PDL, EMA 5/15 alignment.
  * **Right: Live Risk & Breaker HUD (Internal)** *(Replaces static Mission Principles)*:
    * Loss Streak Circuit Breaker: `● ● ● [0/3 Losses]` (trips hard stop on 3 losses).
    * Daily Drawdown Meter: Live progress bar (`₹0 / ₹15,000 Cap Used`).
    * Active In-Position Mini-HUD: Shows live open position (`NIFTY 24600 CE · 2 Lots · P&L: +₹1,200`) with 1-click jump to Workstation.
* **Row 2 (Performance vs Active Safety)**:
  * **Left: Cumulative Equity & Today's Trades**:
    * Clean SVG Cumulative Equity curve.
    * Today's Trades Mini-Table (Fills executed today with timestamp, contract, points, R-multiple).
  * **Right: Active Alerts & Session Checklists**:
    * Live Rule Engine alerts & cool-down countdown timer.
    * Collapsible Pre-Open status and End-of-Day closing review checklist.

---

## 2. Tab 2: Decision Engine (`view-decision`) — LOCKED
* **The "Price Action Decision Matrix" (Replaces 30 dropdowns with 5-sec flow)**:
  * **Step 1: Context (Kind of Day)**:
    * 3 Large Buttons: `[ 📈 TREND ]`, `[ ↔️ TR (RANGE) ]`, `[ 🧱 TTR (CHOP / SOH LOCKED) ]`.
    * Sub-contexts to handle: *Weak / Drag Trend*, *Trending TR*, *Big Range Day in TR*, *Bull Leg in Bear Trend & vice versa*.
  * **Step 2: Location (Non-Negotiable)**:
    * If Trend: `At/Near EMA (5/15)` or `FBO of TL` (YES / NO). Extended away from EMA is blocked as LPT!
    * If TR: `At Range Extreme (Day H-L / Swing H-L)` (YES / NO). Middle of range / EMA in TR is blocked!
  * **Step 3: Signal Bar (Secondary Confirmation)**:
    * `Strong Trend Bar` / `Pause/Doji/Trap` / `Weak Bar`.
    * Rule: If Context & Location are pristine, signal bar form is discounted; execution is permitted.
  * **Step 4: Dynamic A+ Setup Selector (Context-Filtered)**:
    * In Trend: Displays ONLY Trend setups (`BO-1Pb`, `1st Deeppb`, `Deeppb5-15`, `CT 2nd Leg Failure @ EMA`, `EMA/FBO of TL`, `Trend Resumption`).
    * **Counter-Trend (CT) Trades are HARD-LOCKED** with a red padlock shield until valid context shift occurs.
    * In TR: Displays ONLY Range setups (`DT-DB-2LR @ Extreme`, `Rev from 2nd Leg TCL`, `Bull/Bear Leg`, `Failure Rev 2nd Leg TCL`).
  * **Step 5: Staging & Single-Click Execution Gate**:
    * Contract: `NIFTY 23200 CE` | Lots: Auto-synced from Risk Engine.
    * Bracket Preview: Entry ₹145 | SL with **+8 pt noise buffer** | T1 `min(2R, 20 pts)` (auto-moves SL to Break-Even) | T2 Runner.
    * **`⚡ AUTHORIZE MARKET ENTRY & SPAWN BRACKET`** (Flattrade live market fill + AmiBroker chart snapshot).
    * Immediately morphs into **Active Trade In-Position HUD** with 5-min candle confirmation monitor (`Bar 1 Quality`, `Bar 2 Quality`, `Scratch Alert`, and `FOL Premature Exit Guard`).

---

## 3. Tab 3: Risk Engine (`view-risk`) — LOCKED
* **Rupee-First Reality (Replaces Abstract % Simulation)**:
  * **Module 1: Capital Deployment Bar**: Visual stacked bar showing Risk at Stake (₹), Option Margin Required (₹), and Protected Reserve (₹). "Two Futures" cards showing +₹7,500 Win vs -₹3,750 Loss.
  * **Module 2: The 3-Bullet Chamber**: Visual 3-loss slots showing exact rupee burn (`Loss 1: -₹3,750` -> `Loss 2: -₹7,500` -> `Loss 3: -₹11,250 [SESSION LOCK]`). Shows safety buffer before the ₹15,000 daily limit.
  * **Module 3: Drawdown Reality Ladder**: Visual capital steps in hard ₹ (`5% DD: -₹25,000` | `10% DD: -₹50,000` | `15% DD: -₹75,000` | `20% DD: -₹1,00,000`) with live equity needle showing exact distance in ₹ to next tier.
  * **Module 4: Real Rupee Growth Milestones**: `₹5.0L ──► ₹5.5L ──► ₹6.25L ──► ₹7.5L` with sizing upgrades unlocked at each milestone and floor defense at -5%.
  * **Module 5: Interactive Stress-Test Slider**: Real-time "What if I take 4 losses in a row?" calculation showing rupee drawdown and winning trades needed to recover.

---

## 4. Tab 4: Trade Journal (`view-journal`) — LOCKED
* **Auto-Populate Costs & Taxes into Final P&L**:
  * Auto-calculates statutory charges (Brokerage, STT, Exchange turnover, GST, Stamp duty, SEBI).
  * Displays: `Gross P&L` | `Est. Statutory Charges` | `Net Real P&L`.
  * Dedicated button: `[ 📄 Reconcile from Contract Note (CN) ]` to enter exact net payout from PDF.
* **Off-Desk & Mobile Phone Trade Support**:
  * `[ 🔄 Sync Today's Fills from Broker ]`: Auto-pulls orders placed on mobile or other PC into journal queue.
  * Fast manual CN entry for offline logging.
* **1-Click Psychological In-Trade Timeline**:
  * Pre-Entry Mindset (`Calm`, `FOMO`, `Anxious`, `Revenge`).
  * In-Trade Timeline tags (`FOL`, `In The Zone`, `Stop Honored`).
  * Post-Exit State (`Calm`, `Frustrated`, `Euphoric (Greed Alert)`).
* **Advanced Metrics**: Process Adherence Grade (`A+ Disciplined` vs `Rule Breach`), MFE Capture Ratio %, Peak Giveback ₹, Time in Trade & candle count.
* **Missed Opportunity Logger with Visual Chart**:
  * `[ ⚠️ Log Missed Opportunity (FOL / Distraction) ]`.
  * Logs Setup, Root Blocker (`FOL`, `Social Media`), and **Forfeited Profit in Real ₹**.
  * **Attached Chart Evidence**: Clipboard paste (`Ctrl + V`) or 1-Click AmiBroker snapshot. Displays in Journal table with amber/purple badge and full dossier review.

---

## 5. Tab 5: Session Checklists (`view-session`) — LOCKED
* **Pre-Open Strategy Gateway**: System auto-pulls GIFT Nifty gap, PDC, PDH, PDL, 5/15 EMA; trader simply selects Kind of Day expectation, default setup, and invalidation thesis.
* **15-Second Hourly Focus Pulse (10:15, 11:15, 12:15, 13:15, 14:15, 15:15)**:
  * Replaces 168 dropdowns!
  * AEGIS auto-generates 1-hour range, EMA posture, and trade telemetry.
  * Trader does 3 quick taps: Mental State (`Locked In` / `SM Distracted`), Chart Clarity (`Clear` / `Chop`), Next Hour Action (`A+ Only` / `SOH`).
* **Earned 5-Minute Telegram Pass (Pomodoro with Telemetry)**:
  * 55 minutes of focus earns a 5-minute sanctioned break.
  * `[ ⏱️ Activate 5-Min Telegram Pass ]` countdown timer. Chimes when over; tracks unscheduled overtime leakage in red.
  * Correlates Telegram leakage with trade win rate in Analytics.
* **Rupee Leakage Ledger**: Tracks both Execution Mistakes (-₹) and Missed Opportunities (+₹ forfeited).

---

## 6. Tab 6: Analytics (`view-analytics`) — LOCKED
* **4 Organized Clusters**:
  * **Cluster A: Core Edge & Quant**: Win Rate, Expectancy (R and ₹), Profit Factor, Payoff Ratio, SQN, Sharpe, Sortino, Max DD, R-Distribution histogram.
  * **Cluster B: Price Action Matrix**: Performance by Context (Trend vs TR vs TTR), Performance by Location (At EMA vs Extended), Setup profitability ranking, MFE Capture %.
  * **Cluster C: Behavioral & Focus Analytics**: Disciplined vs Undisciplined P&L (Discipline Dividend), Focus/Telegram correlation (Win rate locked-in vs post-Telegram), Rupee Leakage Ledger.
  * **Cluster D: Edge Drift & Early Warning Radar**: Rolling 20-trade health vs baseline, Time-of-day and Day-of-week sweet spots.

---

## 7. Tab 7: Psychology (`view-psychology`) — LOCKED
* **Jared Tendler A/B/C Model**:
  * Live Gaussian Bell Curve with active daily needle and historical dots.
  * Early Tilt Radar: Alerts when a loss + FOMO tag occurs within 20 mins.
  * Financial Cost of Emotions: P&L in ₹ by emotional state (Calm `+₹48k` vs FOMO `-₹11k`).
  * 14-Day Rolling Game Streak Ribbon.

---

## 8. Tab 8: Discipline Protocol (`view-discipline`) — LOCKED
* **Trigger-Active If-Then Rules**: Rules highlight live when triggers occur (e.g. 2nd loss activates 15-min lockout response).
* **60-Second Guided Box Breathing Reset**: Visual expanding/contracting circle linked directly to Active HUD on stop-out.
* **Auto-Surfaced Expensive Mistake of the Week**: Automatically pulls worst off-plan trade with -₹ loss and AmiBroker chart into weekly review.
* **Daily Discipline Gut-Check**: 10-sec close tally.

---

## 9. Tab 9: Market Events (`view-news`) — LOCKED
* **Event Sentinel & Execution Guardrails**:
  * High-impact schedule: RBI MPC, Heavyweight market-hours earnings, FOMC, Union Budget.
  * Automated lockouts on Tab 2: RBI Lockout till 11 AM, 5-min vol window, Mandatory NTD on Budget.
  * Emergency Breaking News Flash Banner (`🚨 BREAKING FLASH`).
  * Clean backend-streamed RSS headlines (ET, Moneycontrol, BS).

---

## 10. Tab 10: Reports (`view-reports`) — LOCKED
* **Executive PDF Generator**: Clean `@media print` reports for Weekly, Monthly, Performance, and Risk reviews.
* **Integrated Metrics**: Discipline Dividend, Rupee Friction summary, Telegram focus integrity score.
* **1-Click Single Trade Dossier Export**: 1-page printable dossier with AmiBroker chart and psychological timeline.

---

## 11. Tab 11: Settings & Rulebook (`view-rulebook`) — LOCKED
* **Plug & Play Broker-Agnostic Adapter (`IBrokerAdapter`)**:
  * Active Broker Dropdown: `[ Flattrade ]`, `[ Zerodha ]`, `[ Dhan ]`, `[ Fyers ]`, `[ Shoonya ]`.
  * Feed API Key & Secret -> Instant 30-sec broker switch with zero UI rewrites.
* **Permanent Home for Mission Principles**: Full core principles and color system moved here to keep Home 100% active.
* **Telegram & Focus Chamber Settings**: Daily budget and break timer configs.
* **Data Backup & Restore**: JSON & CSV export/import with pre-flight verification card.

---

## 12. Tab 12: Replay Lab & Setup Feeder Pipeline (`view-replay-lab`) — SPECIFICATION & ROADMAP
* **Dual Sheet AmiBroker Routing Architecture**:
  * **Live Trade Capture (Sheet 1)**: Locked strictly to Sheet 1 (`NIFTY-I 5m` live chart). Uses current IST system clock, multi-screen extended monitor capture, and real broker order IDs.
  * **Bar Replay Capture (Sheet 3)**: Locked strictly to Sheet 3 (`NIFTY-I 5m` Bar Replay simulator). Extracts exact historical candle timestamp (`YYYY-MM-DD HH:MM:SS`, e.g. `2026-01-01 14:49:59`) from the replayed candle instead of the system clock. Stored in dedicated replay storage without contaminating live trading journal stats.
* **Mathematical Option Translation & Safety Buffer Engine**:
  * **Option Target Move**: $\text{Option Move (pts)} = \text{Futures Move (pts)} \times 0.40$ (40% delta rule; 40 pt Fut move = 16 pt Opt move).
  * **Option Stop-Loss with Safety Buffer**: $\text{Option SL (pts)} = (\text{Futures SL distance} \times 0.40) + 7\text{ pts additional market noise buffer}$ (e.g. 20 pt Fut SL = 8 + 7 = 15 pt Opt SL).
  * **1-Lot Rupee Risk/Reward Calculator**: Auto-computes ₹ Risk, ₹ Reward, and R:R ratio for 1 lot (Nifty 65 qty).
* **Weekly Performance Scorecard (Core Emphasis)**:
  * Aggregated by Trading/Calendar Week (Week 1, Week 2, etc.).
  * Tracks Weekly Win Rate, Weekly Expectancy, Weekly Points Harvested in Options, and Setup Frequency.
  * Identifies top-performing Al Brooks setups per market regime.
* **Deliberate Practice Time Tracker ("Hours on Replay")**:
  * Built-in active session timer & stopwatch for Bar Replay study sessions.
  * Weekly practice metric: Displays total weekly replay hours against practice targets (e.g. 5 hrs/week).
  * Setup discovery efficiency (setups spotted per hour of study).
* **Replay Psychology & Emotional Tagging**:
  * Mindset capture at setup identification: Hesitation Flag, Chasing/FOMO rating, Entry Confidence (1–5 stars).
  * Measures execution friction before risking real capital.
* **Automated Ground-Truth Feeder into `Nifty_Quant_Architect`**:
  * 1-Click export to `D:\Project-Python\Nifty_Quant_Architect\data\training_setups.jsonl`.
  * Feeds 5-min candle metrics (CLV, Real Body, Range, Wicks, Volatility Regime) directly into the quant automation backtesting and auto-execution engine.
