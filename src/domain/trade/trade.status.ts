/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Lifecycle Status
 * ============================================================
 */

export const TRADE_STATUS = {
  Draft: "Draft",
  Planned: "Planned",
  Ready: "Ready",
  Triggered: "Triggered",
  Active: "Active",
  Scaling: "Scaling",
  Completed: "Completed",
  AwaitingReview: "AwaitingReview",
  Reviewed: "Reviewed",
  Archived: "Archived",
} as const;

export type TradeStatus = (typeof TRADE_STATUS)[keyof typeof TRADE_STATUS];
