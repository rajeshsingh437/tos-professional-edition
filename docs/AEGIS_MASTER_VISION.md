# AEGIS MASTER VISION

**Status:** Canonical Vision / Philosophy
**Purpose:** Single source for AEGIS philosophy, long-term intent, and product-level principles.

> This document defines **why AEGIS exists and what it is meant to become**. It does not replace the Constitution, Architecture Rulebook, or CORE-4. Those documents have narrower authority as defined below.

---

## 1. Mission

AEGIS is a **Trading Discipline Operating System**, not merely a trading platform.

Its purpose is to enforce discipline, protect capital, automate a proven trading process, eliminate repetitive work, capture trading data, and provide intelligence for continuous improvement.

## 2. Core Philosophy

The intended AEGIS flow is:

**Market → Trade Plan → Risk Validation → Psychology Validation → Session Validation → Execution Permission → Broker**

The central idea is that trading should be a controlled process rather than an impulsive sequence from chart to order.

The Guardian Engine is the discipline and risk authority. The broker remains the execution venue.

## 3. Guardian Philosophy

Guardian is not simply another UI module. It is the rule-driven control layer through which trading permission is earned.

The long-term concept is:

**SENTRY → Extract Knowledge → Guardian Rules → Guardian Engine → AEGIS**

SENTRY is therefore treated as the first knowledge source for Guardian, not as a system whose screens or business logic should simply be copied into AEGIS.

The Guardian Knowledge Base (GKB) is intended to contain structured knowledge covering:

- Mission
- Trading Philosophy
- Session Rules
- Market Regimes
- Setup Library
- Decision Rules
- Risk Rules
- Psychology Rules
- Trade Management Rules
- Analytics Rules
- Reports
- Rulebook

These are business rules and knowledge. Software modules implement them later.

## 4. Rule Philosophy

Guardian rules should be structured and testable. The intended rule metadata includes:

- Rule ID
- Purpose
- Category
- Priority
- Mandatory
- Blocking
- Dependencies
- Inputs
- Outputs
- Automation Level

A rule must have a clear effect on the system, such as ALLOW, CAUTION/WARN, or BLOCK.

Rules are not to be casually optimized after individual trades. The AEGIS learning philosophy freezes trading rules through a completed **20-trade review cycle** before changes are permitted.

## 5. Trading Session Philosophy

The trading day is stateful and controlled.

The conceptual lifecycle is:

1. Locked
2. Pre-Market Planning
3. Open Validation
4. Entry Validation
5. Protection Enforcement
6. Trade Management
7. Session Control
8. End-of-Day Review

The pre-market process is especially important because it determines whether the planned session conditions exist before execution permission is considered.

## 6. Pre-Market Ritual

The SENTRY upper dashboard is intended to be part of the pre-market ritual, not merely a collection of quote cards.

### Row 1 — Indian Market

- NIFTY
- BANKNIFTY
- SENSEX
- INDIA VIX
- CRUDE
- USD/INR

### Row 2 — Global Market

The dashboard should present major US and Asian market indices and a concise global-market interpretation.

The intended context includes:

- ALIGNED
- NEUTRAL
- potentially MISALIGNED
- Major Event
- News Risk
- Pre-Market Assessment

This context feeds the Guardian pre-market chain:

**Global Cues → Gap Analysis → VIX → Bias → A+ Setup Checklist**

The exact scoring/threshold logic for Global Market interpretation must be explicitly specified before automation; it must not be invented by UI code.

## 7. Broker Philosophy

The broker is an execution venue and market-connectivity authority. AEGIS owns decision-making, risk, execution permission, trade management, automation, journaling, analysis, and protection within its architectural boundaries.

AEGIS must not become a replacement broker terminal.

Broker integration is to be treated as a certification track: capabilities are verified explicitly rather than declared complete by assumption.

## 8. Automation Philosophy

Automation should enforce predefined rules rather than create discretionary behaviour.

Capital protection comes before profit.

Every important action should be explainable, rule-driven, and auditable.

The system should minimize repetitive manual administration while keeping the human trader in the intended decision/oversight role.

## 9. Engineering Philosophy — Mandatory Working Constraints

These are project-level constraints requested by the project owner and must be preserved as governing workflow rules.

### 9.1 Command-Only Rule

Implementation work must use explicit, user-approved commands/actions.

Because the project owner is not from a technical background:

- commands must be simple and copy/paste-ready;
- the purpose of a command must be clear;
- expected results must be stated;
- complete replacement files should be preferred over partial snippets when practical;
- no silent architectural, dependency, configuration, repository, or runtime changes;
- do not infer authorization for a technical action merely because it appears to be the next logical step.

### 9.2 Free-Mode-Only Constraint

AEGIS is to be developed within the user's available **free-mode ChatGPT workflow** because of personal constraints.

During an active engineering task, do not recommend Work Mode, other modes, paid plans, upgrades, or alternative paid options/tools. If a requested operation is technically impossible under the current environment, state the limitation plainly; do not turn the limitation into a sales or upgrade path.

### 9.3 No Repeated Discovery

Once a file/component has been inspected and its verified architecture, responsibilities, dependencies, interfaces, current state, and decisions have been recorded, do not repeatedly re-inspect it unless:

- there is concrete evidence that it changed;
- the recorded state is insufficient for the current task; or
- the current task exposes a genuine contradiction.

The goal is implementation, not endless rediscovery.

## 10. Source-of-Truth Hierarchy

AEGIS documentation is intentionally reduced to four governing working files:

### 1. AEGIS_MASTER_VISION.md

**Authority:** WHY / WHAT / Philosophy / long-term product intent.

### 2. AEGIS_Project_Constitution_v1.0.md

**Authority:** Non-negotiable constitutional principles and safety/risk rules.

### 3. AEGIS_Architecture_Rulebook.md

**Authority:** HOW the system is architecturally structured and where responsibilities belong.

### 4. AEGIS_CORE_4.md

**Authority:** Current verified implementation state, handoffs, completed work, known blockers, and next implementation step.

CORE-4 is **not** a second architecture document. It must not silently redefine philosophy or architectural rules.

Historical documents, chats, screenshots, task notes, implementation logs, and archived material are references only. They cannot silently override the four canonical files.

## 11. Architecture Gate — Preventing Drift

Before implementation of a non-trivial engineering task, answer these five questions:

1. **What are we changing?**
2. **Where is the authoritative specification?**
3. **What does CORE-4 say about the current implementation state?**
4. **Does the requested change contradict the Constitution or Architecture Rulebook?**
5. **What is the single implementation owner?**

If the answer to #4 is unclear, stop implementation and reconcile the architecture first.

If an old discussion conflicts with a canonical file, do not silently choose a side. Mark the item **UNRESOLVED / PENDING ARCHITECTURAL DECISION** until explicitly decided.

## 12. Definition of a Healthy Work Session

A healthy AEGIS engineering session should look like:

**Read canonical source → confirm current state → make the smallest correct change → test → record result → update CORE-4 → continue.**

It should not look like:

**Repeated verification → repeated discovery → repeated architecture discussion → no implementation.**

## 13. Long-Term Goal

AEGIS should become a durable trading discipline and intelligence system in which the trader's process is captured, protected, measured, learned from, and continuously improved without allowing short-term outcomes or ad-hoc technical decisions to redefine the system's philosophy.

---

## Authority Notice

This document is the canonical **Vision/Philosophy** source. It does not override the Constitution or Architecture Rulebook on matters within their authority.

Any future architectural change must be explicitly reconciled and recorded rather than introduced through a work note, chat message, or implementation shortcut.
