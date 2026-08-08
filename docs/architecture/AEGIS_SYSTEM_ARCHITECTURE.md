# AEGIS System Architecture

## Purpose

This document is the single source of truth for the AEGIS architecture.

## Core Principles

- Single Responsibility
- One Source of Truth
- Architecture before implementation
- No duplicate implementations
- Engines communicate through interfaces/Event Bus
- Git is the history; no backup files.

## Repository Structure

```text
AEGIS/
├── app/
├── config/
├── docs/
├── external/
├── server/
├── src/
│   ├── core/
│   │   ├── broker/
│   │   ├── market_data/
│   │   ├── automation/
│   │   ├── risk/
│   │   ├── portfolio/
│   │   ├── analytics/
│   │   ├── event_bus/
│   │   ├── screenshots/
│   │   └── notifications/
│   └── tests/
└── ui/
```

## Broker Engine

Authentication, OAuth, Relay, Orders, Positions, Holdings, Limits,
Broker WebSocket.

## Market Data Engine

AmiBroker integration, realtime feed, historical data, option chain,
future providers.

## Oracle Relay

Independent deployment.

## Git

Ignore config/broker.json, config/session.json and tokens.json. Commit
broker.example.json.

## Working Rules

- Mini tasks.
- Environment first.
- Commands before explanation.
- State limitations.
- No background work claims.
- Automatic progression unless user requests a break.
