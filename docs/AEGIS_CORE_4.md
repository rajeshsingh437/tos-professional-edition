# AEGIS CORE-4

**Status:** Canonical Current-State / Implementation Handoff  
**Role:** Records verified implementation state, handoffs, blockers and the exact next implementation step.

## 1. Governing Documents

AEGIS is governed by exactly four working documents:

1. `AEGIS_MASTER_VISION.md` — WHY / WHAT / philosophy / long-term intent.
2. `AEGIS_Project_Constitution_v1.0.md` — constitutional and safety rules.
3. `AEGIS_Architecture_Rulebook.md` — HOW the architecture works and ownership boundaries.
4. `AEGIS_CORE_4.md` — current verified state and implementation handoff.

Historical notes, chats, screenshots, task notes and archives are reference material only and do not override these four files.

## 2. Mandatory Working Rules

- Command-only engineering workflow.
- Commands must be simple and copy/paste-ready.
- No silent architectural, dependency, configuration, repository or runtime changes.
- Prefer complete replacement files when practical.
- Do not repeatedly rediscover verified files/components unless there is evidence of change, insufficient recorded state, or a genuine contradiction.

## 3. SESSION CONTINUITY PROTOCOL — MANDATORY

This section exists to eliminate repeated inspection, repeated audits and loss of the exact stopping point between sessions.

### 3.1 Start Every Session Here

Read CORE-4 first and identify:

1. current phase;
2. active task;
3. exact stopping point;
4. already-verified files/components;
5. decisions already made;
6. blockers;
7. exact next concrete implementation action.

Do not restart discovery merely because a new session has started.

### 3.2 One Inspection → Permanent Reference

Once a file/component has been inspected and its verified architecture, responsibility, dependencies, interfaces, current state and decisions are recorded, consider it **VERIFIED**.

Re-inspect only when:

- the implementation changed;
- a test/runtime result contradicts the record;
- the record is insufficient for the current task; or
- a genuine architectural/interface contradiction appears.

### 3.3 Required Workflow

`CORE-4 → relevant canonical specification → exact current task → implementation`

Never default to:

`CORE-4 → rediscover project → inspect everything → audit everything → discuss architecture again`

### 3.4 Session-End Record

Before ending a meaningful engineering session, update CORE-4 with:

- work completed;
- files changed;
- newly verified files/components;
- decisions made;
- tests performed;
- blockers;
- exact stopping point;
- one concrete next implementation action.

The next action must be precise enough that the next session can start implementation immediately.

### 3.5 No Repeated Task Rule

Completed work is not repeated unless regression, implementation change, a new requirement, or a previously provisional result requires it.

## 4. Confirmed SENTRY Runtime Path

`app/main.py`
→ `app/sentry_bridge.py`
→ `migration/dashboard/boot.html`
→ `migration/dashboard/index.html`
→ SENTRY dashboard in pywebview.

`ui/dashboard.py` and `ui/widgets/market_card.py` were inspected during the August 14 investigation but are not the active SENTRY dashboard path.

## 5. Verified Canonical Market-Data Flow

**Flattrade WebSocket → FlattradeAdapter → TickNormalizer → MarketTick → EventBus → MarketDataService**

Verified NIFTY realtime payload included:

- `e = NSE`
- `tk = 26000`
- `ts = Nifty 50`
- `lp = 24366.00`
- `c = 24395.85`
- `pc = -0.12`

The broker `c` field is the valid previous-close value. The realtime `pc` field must not be treated as `MarketTick.previous_close`.

`TickNormalizer` was corrected accordingly and a valid canonical `MarketTick` was constructed.

The tick is stored by `MarketDataService` under:

`('NSE', '26000')`

`SentryApi.market_data_get_latest('NSE', '26000')` returns the canonical `MarketTick`.

Integer token `26000` is not the canonical lookup form; callers must use the string token.

## 6. Verified Components — DO NOT RE-INSPECT

Already verified:

- `src/core/broker/adapters/flattrade_adapter.py`
- `src/core/broker/services/websocket_manager.py`
- `src/core/events/tick_normalizer.py`
- `src/core/events/market_tick.py`
- `src/core/events/event_bus.py`
- `src/core/market/market_data_service.py`
- `src/core/broker/broker_manager.py`
- `app/sentry_bridge.py`

Re-inspection requires one of the exceptions in Section 3.2.

## 7. SENTRY Dashboard Handoff

The active SENTRY dashboard already exists and is functional.

The next implementation is the upper market-context area. Preserve the existing SENTRY visual language. Do not rebuild the dashboard.

### Row 1 — Indian Market

- NIFTY
- BANKNIFTY
- SENSEX
- INDIA VIX
- CRUDE
- USD/INR

### Row 2 — Global Market

- Major US indices
- Major Asian indices
- Global-market interpretation

### Context / Pre-Market Interpretation

- ALIGNED
- NEUTRAL
- potentially MISALIGNED
- Major Event
- News Risk
- Pre-Market Assessment

This is part of the pre-market ritual, not merely decorative quote display.

Guardian chain:

**Global Cues → Gap Analysis → VIX → Bias → A+ Setup Checklist**

Exact scoring/threshold rules for global interpretation are not yet canonical. Do not invent them in UI code.

## 8. Market-Data Ownership

Live Market Data belongs to AEGIS Core. Dashboard belongs to Intelligence.

Production flow:

**Broker market data → AEGIS Core / Event Engine → canonical MarketTick/EventBus → SENTRY UI bridge → market display**

Legacy SENTRY external quote fetching must not become the canonical market-data architecture.

## 9. Architecture Gate

Before non-trivial implementation, confirm:

1. What is changing?
2. Which canonical document specifies it?
3. What does CORE-4 say is already verified?
4. Does the change conflict with Constitution or Architecture Rulebook?
5. Which component owns the change?

Resolve ambiguity once and record the result here.

## 10. CURRENT WORK STATE

### Documentation Continuity
**COMPLETE**

Continuity is now part of CORE-4. No fifth governing document is introduced.

### UI Dashboard
**ACTIVE**

SENTRY upper-dashboard implementation is now active and must use the verified canonical market-data path.

### First UI Target

Implement the Indian market context row:

NIFTY → BANKNIFTY → SENSEX → INDIA VIX → CRUDE → USD/INR

Start from the verified NIFTY path. Confirm canonical broker tokens/data sources for the remaining instruments before wiring them.

## 11. EXACT NEXT IMPLEMENTATION ACTION

**Connect the verified canonical `MarketTick` path to the existing SENTRY dashboard/UI bridge and implement the first Indian-market context row, beginning with NIFTY.**

Do not restore legacy external quote fetching.

Do not rebuild the dashboard.

Do not invent unapproved market-scoring rules.

## 12. SESSION END UPDATE

After every meaningful implementation step, update:

- verified result;
- files changed;
- test result;
- new dependency/interface;
- blocker;
- exact stopping point;
- next concrete implementation step.

**Current Handoff:** Documentation continuity established. SENTRY upper-dashboard implementation is active and should continue from the verified canonical market-data path.
