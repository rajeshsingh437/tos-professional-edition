# Changelog

All notable changes to this project will be documented here.

---

## Build 0.2.004 (2026-09-27)

### Added
- **Phase 11: Settings & Rulebook Engine**:
  - **Plug & Play Broker Adapter (`IBrokerAdapter`)**: Unified interface supporting Flattrade (Noren Zero Brokerage), Zerodha (Kite3), Dhan HQ (Direct v2), Fyers (API v3), and Shoonya (Noren Zero).
  - **Broker Telemetry Diagnostics Console**: Real-time diagnostic console for testing Authenticate, Positions, Orders, Trades, Limits, and Demat Holdings.
  - **Auto-Populated Verified Credentials**: Pre-loads Flattrade account (`FZ02894`) and Oracle VM relay (`http://130.210.22.73:8091`).
  - **Al Brooks Setup Atlas**: Searchable visual library of 10 core price action setups across Breakout, Reversal, Range, and High Volatility categories.
  - **Telegram Sentinel & Focus Chamber Settings**: Interactive budget and break duration controls.
  - **Data Backup & Restore Engine**: Pre-flight verification card displaying record counts and timestamps before committing imports.
- **Clean Slate Testing Mode**:
  - `tos_fresh_slate` lock preventing resurrecting of seed trades after a user reset.
  - KPI banner updated to display clean dashes (`—`) when trade count is zero for Monday 1-lot live testing.
- **Python SentryApi Native Handlers**:
  - Exposed live `flattrade_login`, `flattrade_positions`, `flattrade_orders`, `flattrade_trades`, `flattrade_limits`, and `flattrade_holdings` methods in `app/sentry_bridge.py`.
- **Phase 12 Architecture Specification: Replay Lab & AmiBroker Setup Feeder**:
  - Sheet 1 (Live Multi-Monitor) vs Sheet 3 (Bar Replay) auto-routing.
  - Option move translation ($40\%$ delta rule) and Stop-Loss safety buffer ($+7\text{ pts}$).
  - Weekly Performance Scorecard and Deliberate Practice hours tracker.
  - Ground-truth export pipeline to `Nifty_Quant_Architect`.

---

## Build 0.2.003 (2026-09-26)

### Added
- **Market Context Engine**: 7-card trader hierarchy (`GIFT NIFTY` → `NIFTY 50` → `BANK NIFTY` → `SENSEX` → `INDIA VIX` → `CRUDE` → `USD / INR`).
- **GIFT Nifty Implied Gap**: Real-time gap points and percentage relative to Nifty spot.
- **Nifty-First Volatility**: Daily expected Nifty points swings from India VIX (`±185 pts · Standard ATR`) and volatility sizing tiers.
- **Macro Risk Engine**: Real-time evaluation for Spiking Brent Crude (`CRUDE SPIKE` / OMC & Paint drag) and Depreciating Rupee (`INR FALLING BIG` / FII outflow drag).
- **Flattrade Broker Integration**: Replaced third-party web scraping with native Flattrade REST/WebSocket feeds, `sentry_bridge.py` fallback, and FastAPI `/api/market-context` endpoint.
- **Institutional Event Radar & Breaking News Flash**: Auto-counting event engine with dismissal banner and simulator buttons.

---

## Build 0.2.0-alpha.2

Status

In Development

### Added

- Design system
- Layout architecture
- React Router
- Modular CSS structure
- Project documentation

### Planned

- Professional Sidebar
- Professional Header
- Dashboard redesign
- UI Component Library

---

## Build 0.1.x

### Added

- React + Vite setup
- Sidebar
- Header
- Dashboard prototype
- Navigation
- GitHub integration
