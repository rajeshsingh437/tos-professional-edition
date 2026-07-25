# TLE – Proposed Changes v1.1

**Base Document:** TLE – Trade Object & Trade Lifecycle Specification, FROZEN v1.0
**Status of this document:** PROPOSED — not merged, not yet approved
**Rule followed:** Per the v1.0 Freeze Rule, no edits have been made to the frozen document.
All amendments below are recorded separately, as required, for discussion after
the current implementation milestone completes.

---

## How to use this document

Each item below states: the gap in v1.0, the proposed change, and the reason it matters
for TOS specifically (Nifty options, discretionary execution, process-over-outcome
philosophy). Nothing here is auto-approved — treat each item as a separate decision.

---

## 1. Field Data Types & Validation

**Gap:** v1.0 names fields (e.g. "Maximum Risk," "Position Size") but specifies no type,
required/optional status, or validation rule. This is the single largest blocker to a
consistent implementation.

**Proposed change:** Every field in every section gets a type contract before coding starts.
See the accompanying `trade-object.types.ts` for a full first draft.

**Why it matters:** Without this, the Rule Engine and Analytics suite can't trust the data —
e.g. "Maximum Risk" could be entered as ₹, %, or R-multiple depending on who fills the form.

---

## 2. Instrument / Contract Object

**Gap:** No explicit field set for the traded instrument. For Nifty CE/PE trades, strike,
expiry, option type, and lot size are the difference between a valid trade record and a
useless one — right now they'd have to be crammed into "Strategy" or "Market Context" as
free text.

**Proposed change:** Add a new top-level section, **Instrument**, referenced by every
other section instead of duplicating instrument details in Planning/Execution.

Fields: Symbol, Instrument Type (Index / Stock), Option Type (CE / PE), Strike Price,
Expiry Date, Lot Size, Contract Multiplier.

**Why it matters:** This is what lets the Risk Engine calculate premium outlay in INR and
lets Analytics slice performance by strike distance, DTE, or expiry week — all things your
existing TOS v2 Risk Engine already assumes exist.

---

## 3. Execution & Exit as Leg Arrays (not Entry 1–4 / Exit 1–4)

**Gap:** Hardcoded Entry 1–4 and Exit 1–4 fields cap every trade at four legs and hardcode
the shape of scale-in/scale-out logic.

**Proposed change:** Replace with an array of leg objects:
`{ legId, price, quantity, timestamp, orderType }` for both entries and exits. Average
Entry / Average Exit become computed fields, not stored fields.

**Why it matters:** Removes an arbitrary cap, and average price becomes derived (always
correct) instead of manually reconciled.

---

## 4. Explicit Boundary: Execution vs. Trade Management

**Gap:** It's undefined whether a 5th add-on entry after the initial fill belongs in
Execution or in Trade Management ("Added Quantity").

**Proposed change:** Rule: **Execution** holds every leg that fills the *original* trade
thesis (the planned entry). **Trade Management** holds every leg that modifies a trade
*already Active* — i.e., anything added/reduced/moved after the trade reaches the
`Active` lifecycle state.

**Why it matters:** Without this rule, the same action could be logged two different ways
by the same trader depending on mood — which defeats the purpose of a Rule Engine trying to
detect deviation from plan.

---

## 5. Readiness Score (Weighted, with Threshold)

**Gap:** The Readiness checklist in v1.0 is a flat list with no scoring or GO/CAUTION/STOP
threshold defined — despite the doc stating this checklist *becomes* that engine.

**Proposed change:** Assign each Readiness item a weight (reuse the ten-item weighted
model from the existing TOS v2 Decision Engine rather than inventing a second, competing
one). Define explicit score bands, e.g.:
- Score ≥ 80 → GO
- Score 50–79 → CAUTION
- Score < 50 → STOP

**Why it matters:** Two competing checklist/scoring models (TOS v2's and TLE's) would
silently drift apart over time. This ties TLE back to the model you already validated.

---

## 6. Lifecycle: Add a Non-Terminal Exit Path

**Gap:** The lifecycle (Draft → Planned → Ready → Triggered → Active → Scaling →
Completed → Awaiting Review → Reviewed → Archived) is purely forward-moving. There's no
state for a trade that was planned and marked Ready but never triggered.

**Proposed change:** Add two branch states:
- **Invalidated** — thesis broke before entry (market moved past the trigger condition)
- **Skipped** — setup was valid and Ready, but the trade was not taken (hesitation, fear,
  distraction)

Both route to Review, same as Completed trades.

**Why it matters:** This is arguably the single highest-value addition for your stated
goal. "Skipped" trades that were objectively valid are a direct, measurable signal of
discipline/execution gap — separate from any trade you actually placed. Right now the
model can't even capture that a valid setup was missed.

---

## 7. Psychology Fields as Fixed Numeric Scales

**Gap:** Emotion Before/During/After, Confidence, Stress, Fear, Greed, Patience,
Distraction have no defined scale — the doc's own example ("show every losing trade where
Confidence exceeded 9/10") assumes a 1–10 scale that is never actually specified.

**Proposed change:** Fix all Psychology fields to an integer 1–10 scale except "Emotion
Before/During/After," which becomes a constrained enum (e.g. Calm, Confident, Anxious,
Frustrated, Euphoric, Fearful, Neutral) rather than free text.

**Why it matters:** Free text can't be aggregated into the mood charts and A/B/C
Self-Check your Psychology Dashboard already relies on. Locking the scale now avoids a
painful data-migration later.

---

## 8. Stage Timestamps for Lifecycle Transitions

**Gap:** No section captures *when* a trade moved between lifecycle states, so decision
latency (time sitting on a valid signal before entry) can't be measured.

**Proposed change:** Add a `lifecycleHistory` array to Identity:
`{ status, timestamp }`, appended automatically on every state transition.

**Why it matters:** This is often where discipline actually breaks — not in the plan
itself, but in the gap between "Ready" and "Triggered." Without timestamps, that gap is
invisible.

---

## Summary Table

| # | Area | Change | Priority |
|---|------|--------|----------|
| 1 | All sections | Add types + validation rules | High — blocks implementation |
| 2 | New section | Add Instrument/Contract object | High — options-specific |
| 3 | Execution/Exit | Convert to leg arrays | Medium |
| 4 | Execution vs Mgmt | Define explicit boundary rule | Medium |
| 5 | Readiness | Add weighted score + GO/CAUTION/STOP thresholds | High — reconcile with TOS v2 |
| 6 | Lifecycle | Add Invalidated/Skipped states | High — direct discipline metric |
| 7 | Psychology | Fix fields to numeric scale / enum | Medium |
| 8 | Identity | Add lifecycleHistory timestamps | Medium |

---

*This document proposes changes only. No changes have been made to
`TLE_Trade_Object_and_Lifecycle_Specification.md`, per its own Freeze Rule.*
