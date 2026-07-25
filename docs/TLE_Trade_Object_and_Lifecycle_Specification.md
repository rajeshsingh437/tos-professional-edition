# TLE – Trade Object & Trade Lifecycle Specification

**Status:** FROZEN v1.0

**Document Status:** Frozen for Implementation

**Rule:**
This document is the single source of truth for the Trade Lifecycle Engine (TLE).
No changes shall be made during implementation.
Any proposed changes shall be recorded separately and discussed only after completion of the planned implementation milestone.

---

# Purpose

The Trade Lifecycle Engine (TLE) is the foundation of the Trading Operating System (TOS).

Every trade is represented as one complete lifecycle, beginning with an idea and ending with learning.

One Trade = One Trade ID.

---

# Trade Object

The Trade Object consists of the following logical sections.

---

# 1. Identity

Every trade must have a permanent identity.

Fields:

- Trade ID
- Created Date
- Created By
- Status
- Version
- Tags

Rules:

- Trade ID never changes.
- Every record references the Trade ID.
- One Trade = One Trade ID.

---

# 2. Planning

Planning represents the reason for taking the trade.

Fields:

- Why this trade?
- What is the edge?
- Strategy
- Timeframe
- Expected Risk Reward
- Maximum Risk
- Maximum Loss
- Position Size
- Capital Allocation
- Market Context
- Supporting Thesis
- Invalidation
- Entry Trigger

Purpose:

This becomes the official Trading Plan.

---

# 3. Readiness

Readiness determines whether the trade should be executed.

Checklist:

- Sleep adequate?
- Emotion stable?
- News checked?
- Economic Calendar checked?
- Trend confirmed?
- Liquidity adequate?
- Risk Reward acceptable?
- Risk within Daily Limit?
- Today's Mindset
- Any Revenge Trading?

Purpose:

This becomes the GO / CAUTION / STOP Engine.

---

# 4. Execution

Execution records every entry.

Fields:

- Entry 1
- Entry 2
- Entry 3
- Entry 4
- Average Entry
- Slippage
- Broker
- Order Type
- Execution Notes

Purpose:

Represents actual order execution.

---

# 5. Trade Management

Trade Management records every modification after entry.

Fields:

- Stop Moved
- Partial Exit
- Scaling
- Added Quantity
- Reduced Quantity
- Reason
- Time
- Emotion
- Confidence

Purpose:

Creates the complete Trade Timeline.

---

# 6. Exit

Exit records every closing transaction.

Fields:

- Exit 1
- Exit 2
- Exit 3
- Exit 4
- Average Exit
- Realised P&L
- R Multiple
- Exit Reason

Purpose:

Represents trade completion.

---

# 7. Review

Trade Review evaluates process rather than financial outcome.

Questions:

- Was the plan followed?
- Was discipline maintained?
- Was sizing correct?
- Did I interfere?
- Was exit emotional?
- Was stop respected?
- Would I take this trade again?

Principle:

Profit ≠ Good Trade

Loss ≠ Bad Trade

Process is evaluated independently.

---

# 8. Psychology

Psychology records the trader's emotional state.

Fields:

- Emotion Before
- Emotion During
- Emotion After
- Confidence
- Stress
- Fear
- Greed
- Patience
- Distraction

Purpose:

Creates long-term behavioural analytics.

Example:

Show every losing trade where Confidence exceeded 9/10.

---

# 9. Learning

Every trade must leave knowledge behind.

Fields:

- Biggest Mistake
- Biggest Success
- Lesson Learned
- Rule Created
- Rule Broken

Purpose:

Continuous improvement.

---

# 10. Attachments

Trade evidence.

Supported Attachments:

- Before Entry Screenshot
- Entry Screenshot
- Management Screenshot
- Exit Screenshot
- Review Screenshot
- Video
- Chart Markups

---

# Trade Lifecycle

Every Trade progresses through the following lifecycle.

Draft

↓

Planned

↓

Ready

↓

Triggered

↓

Active

↓

Scaling

↓

Completed

↓

Awaiting Review

↓

Reviewed

↓

Archived

Important Principle:

Completed ≠ Finished

A trade is complete only after review and learning have been captured.

---

# Three Core Questions

Every Trade must answer three questions.

## 1. Was it a good idea?

Planning

---

## 2. Was it executed well?

Execution

---

## 3. Did I learn something?

Review

These three evaluations are considered more important than the financial result alone.

---

# Why this Model

A properly defined Trade Object allows:

- Trading Journal
- Risk Manager
- Analytics
- AI Coach
- Reports

to operate from a single consistent data model.

Everything in TOS is built upon this foundation.

---

# Independent Scores

Every Trade maintains two separate scores.

## 1. Process Score (0–100)

Measures adherence to the trader's own process and discipline.

---

## 2. Outcome Score

Measures the financial result.

Includes:

- P&L
- R Multiple
- Return
- Win / Loss

Process Score and Outcome Score are intentionally independent.

A profitable trade with poor discipline may receive:

High Outcome Score

Low Process Score

A losing trade executed perfectly may receive:

High Process Score

Low Outcome Score

---

# Freeze Rule

Status: FROZEN v1.0

No additions.

No deletions.

No redesign.

Implementation must follow this document exactly.

Future ideas shall be discussed only after completion of the implementation milestone.
