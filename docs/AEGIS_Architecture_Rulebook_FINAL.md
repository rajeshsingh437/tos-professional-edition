# AEGIS Architecture Rulebook

**Version:** 1.0\
**Status:** 🔒 LOCKED

## Project Definition

> **AEGIS is an Automation and Intelligence Layer that sits on top of
> the broker terminal without replacing it.**

Its purpose is to eliminate repetitive work, automatically capture
trading data, protect the trader through risk controls, and provide
intelligence for continuous improvement.

------------------------------------------------------------------------

# Three-Layer Architecture

## Layer 1 -- Execution (Broker Terminal)

**Flattrade Terminal is the only execution platform.**

Responsibilities: - User Login - Order Entry - Order Modification -
Order Cancellation - Position Management - Manual Square-off

AEGIS does **not** replace the broker terminal.

------------------------------------------------------------------------

## Layer 2 -- Automation (AEGIS Core)

Responsibilities: - Broker Connection Manager - Live Market Data - Trade
Event Engine - Journal Automation - Entry Screenshot Engine - Exit
Screenshot Engine - MAE/MFE Tracking - Charges Engine - Contract Note
Engine - Risk Monitor - Kill Switch

------------------------------------------------------------------------

## Layer 3 -- Intelligence

Built on top of automation: - Dashboard - Analytics - Psychology -
Discipline - Decision Engine - Reports

------------------------------------------------------------------------

# Rule BR-001 -- Broker Integration Philosophy (LOCKED)

## Design Principle

> **AEGIS is NOT a broker terminal.**

The broker terminal remains the single source of trade execution.

AEGIS observes, records, automates, analyzes, and protects.

------------------------------------------------------------------------

# Responsibilities

## Broker Terminal

Responsible for: - Login - Order Entry - Modify Orders - Cancel Orders -
Position Management

## AEGIS

Responsible for: - Live broker connection - Live order & trade
monitoring - Position monitoring - MTM monitoring - Automatic journal
population - Entry & Exit screenshots - MAE/MFE tracking - Provisional
charge calculation - Analytics updates - Psychology & Discipline
updates - Background automation

------------------------------------------------------------------------

# Trade Flow

Trader → Flattrade Terminal → Broker API → AEGIS Event Engine → Journal
→ Screenshots → Risk → Analytics → Psychology → Reports

------------------------------------------------------------------------

# Contract Note Philosophy

Primary Source: - Live broker feed

Fallback Source: - Contract Note import

Use Contract Notes only when: - AEGIS was offline - PC unavailable -
Mobile trading - Another system used - Recovery or verification is
required

Contract Notes are a **backup and reconciliation mechanism**, not the
primary source.

------------------------------------------------------------------------

# Kill Switch Exception

This is the only feature where AEGIS may initiate broker actions.

When configured MTM loss threshold is breached:

-   Cancel pending orders (where supported)
-   Square off positions (where supported)
-   Lock trading inside AEGIS
-   Record the event
-   Notify the trader

------------------------------------------------------------------------

# Rule ENG-001 -- Do Not Duplicate Broker Functionality

AEGIS must never duplicate features the broker terminal already
performs.

Do NOT build: - Order Entry screens - Modify Order screens - Order
Book - Position Window - Trade Window

Instead, focus on: - Automation - Intelligence - Journaling - Visual
evidence - Risk oversight - Coaching - Decision support

------------------------------------------------------------------------

# Engineering Roadmap

## Milestone M1 -- Broker Automation Foundation

1.  Flattrade Connection Manager
2.  Live Event Engine
3.  Automatic Entry Screenshot
4.  Automatic Exit Screenshot
5.  Journal Automation
6.  Kill Switch
7.  Contract Note Recovery

------------------------------------------------------------------------

# Core Vision

> Launch AEGIS.

> Connect to Flattrade once (if required).

> Trade entirely from the broker terminal.

> AEGIS automatically captures, journals, analyzes, and protects
> throughout the session.

No manual administration unless absolutely necessary.
