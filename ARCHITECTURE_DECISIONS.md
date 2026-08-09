# SENTRY Architecture Decisions (Living Document)

**Status:** Approved baseline architecture

## Core Principles

1.  **SENTRY is the only user interface.**
    -   No parallel desktop UI.
    -   All trading workflows are surfaced through SENTRY.
2.  **Oracle Relay is the secure broker gateway.**
    -   SENTRY never communicates directly with Flattrade.
    -   All authenticated broker communication flows through Oracle
        Relay.
3.  **Python is the primary backend language.**
    -   Broker management, authentication, orders, holdings, positions,
        funds, analytics, and business logic remain in Python.
4.  **Go is reserved for one purpose only.**
    -   The Market Data / WebSocket processing engine may be rewritten
        in Go **only if** real profiling under live market conditions
        proves Python is a measurable bottleneck.
    -   Go is not to be introduced based on speculation.

## High-Level Architecture

``` text
SENTRY Dashboard
        │
 PyWebView API
        │
 Python Backend
        │
 Broker Manager
        │
 Oracle Relay
        │
 Flattrade
```

## Future Market Data Engine

``` text
                Broker Manager
                      │
          ┌───────────┴───────────┐
          │                       │
     REST / Session        Market Data Engine
                                │
                        Python (initial)
                                │
                      Replaceable Component
                                │
                      Python  ⇄  Go (if justified)
```

## Broker Manager Responsibilities

-   Login / Logout
-   Session Status
-   Funds
-   Holdings
-   Positions
-   Orders
-   Place / Modify / Cancel Orders
-   Market Data
-   WebSocket lifecycle

The rest of SENTRY must not depend on broker-specific implementations.

## Event-Driven Design

Broker updates are published once and consumed by: - Dashboard -
Portfolio - Risk Engine - Analytics - Journal - Other modules

Avoid duplicate polling and duplicate WebSocket subscriptions.

## Implementation Roadmap

### Milestone 1

-   Oracle Relay
-   Authentication
-   REST endpoints

### Milestone 2

-   Backend integration
-   Broker Manager

### Milestone 3

-   Broker Center
-   Login
-   Live status

### Milestone 4

-   Funds
-   Holdings
-   Positions
-   Orders

### Milestone 5

-   WebSocket
-   Live market data

### Milestone 6

-   Risk Engine
-   Decision Engine
-   Analytics

## Rule

Do not revisit these architectural decisions unless there is compelling
evidence that a different design provides a measurable technical
advantage.
