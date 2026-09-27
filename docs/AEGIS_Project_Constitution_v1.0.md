# AEGIS Project Constitution v1.0

> **Mission:** Build AEGIS as a **Trading Discipline Operating System**,
> not merely a trading platform.

------------------------------------------------------------------------

# Vision

AEGIS exists to enforce discipline, protect capital, and automate a
proven trading process. Every trading action must pass through the
Guardian Engine before reaching a broker.

------------------------------------------------------------------------

# Core Principles

1.  Architecture before Features.
2.  Capital Protection before Profit.
3.  Guardian has final authority over order execution.
4.  Broker APIs only; no UI/screen automation.
5.  One feature → One implementation → One owner.
6.  Broker-independent trading logic.
7.  Automation enforces predefined rules.
8.  Rules change only after a completed 20-trade review cycle.
9.  Every order must be protected.
10. Every major design decision is documented.

------------------------------------------------------------------------

# Architecture Layers

1.  Vision
2.  Constitution
3.  Architecture
4.  Guardian Engine
5.  Trading Engine
6.  Broker SDK
7.  Desktop UI

------------------------------------------------------------------------

# Guardian Engine

## Responsibilities

-   Session Manager
-   Rule Engine
-   Permission Engine
-   Risk Controller
-   Trade Manager
-   Order Engine
-   Position Manager
-   OCO Manager
-   Kill Switch
-   Psychology Monitor
-   Learning Cycle Manager
-   Decision Log

------------------------------------------------------------------------

# Trading Session Lifecycle

## Stage 0 -- Locked

-   Terminal locked.
-   No trading.

## Stage 1 -- Pre-Market Planning

Guardian evaluates: - Global cues - Gap analysis - VIX - Bias - A+ setup
checklist

Result: - PASS → Watch Mode - FAIL → Locked

## Stage 2 -- Open Validation

Only unlock when: - Planned A+ setup exists. - Market matches the
planned scenario.

## Stage 3 -- Entry Validation

Validate: - Position size - Risk - Reward/Risk - Daily limits - Setup
grade - Session state

## Stage 4 -- Protection

Immediately enforce: - Stop Loss - OCO (where applicable) - Money stop -
Manual terminal lock except approved actions

## Stage 5 -- Trade Management

Automate: - Break-even - Partial exits - Trailing stop - Time stop -
Profit protection

## Stage 6 -- Session Control

-   Normal day → Lock after quality trade.
-   Trend day → Permit additional A+ trades only.

## Stage 7 -- End of Day

Generate automatically: - Journal - Analytics - Rule compliance -
Psychology review - Market classification

------------------------------------------------------------------------

# Permission Levels

0.  Locked
1.  Observe
2.  Paper Trading
3.  One A+ Trade
4.  Trend Day
5.  Professional

------------------------------------------------------------------------

# 20-Trade Learning Cycle

Rules remain frozen for twenty completed trades. Only after the review
cycle may trading rules be modified.

------------------------------------------------------------------------

# Broker Philosophy

AEGIS owns: - Decision making - Risk - Execution permission - Trade
management

Broker owns: - Order execution - Market connectivity

------------------------------------------------------------------------

# Mandatory Risk Controls

-   Hard Stop
-   Money Stop
-   OCO
-   Kill Switch
-   Flatten All
-   Cancel All Orders
-   Daily Loss Limit
-   Maximum Trades
-   Maximum Exposure

------------------------------------------------------------------------

# Guardian Decision Log

Every decision records: - Timestamp - Market state - Rule evaluated -
Allow / Warn / Block - Reason - Outcome

------------------------------------------------------------------------

# Definition of Done

Every module must be:

-   Functional
-   Architecturally compliant
-   Independently testable
-   Documented
-   Reusable
-   Free of duplicate business logic

------------------------------------------------------------------------

# Living Document

This document is the constitutional foundation of AEGIS.

Future architecture, code, modules and features must comply with these
principles.
