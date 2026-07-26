/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Status
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

export const TRADE_STATUS = {
  DRAFT: "Draft",
  PLANNED: "Planned",
  READY: "Ready",
  TRIGGERED: "Triggered",
  ACTIVE: "Active",
  SCALING: "Scaling",
  COMPLETED: "Completed",
  INVALIDATED: "Invalidated",
  SKIPPED: "Skipped",
  AWAITING_REVIEW: "AwaitingReview",
  REVIEWED: "Reviewed",
  ARCHIVED: "Archived",
} as const;

export type TradeStatus = (typeof TRADE_STATUS)[keyof typeof TRADE_STATUS];
