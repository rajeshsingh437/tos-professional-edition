/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Management
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

/**
 * Types of trade management events.
 */
export const TRADE_MANAGEMENT_EVENT_TYPE = {
  STOP_MOVED: "STOP_MOVED",
  PARTIAL_EXIT: "PARTIAL_EXIT",
  SCALE_IN: "SCALE_IN",
  SCALE_OUT: "SCALE_OUT",
} as const;

export type TradeManagementEventType =
  (typeof TRADE_MANAGEMENT_EVENT_TYPE)[keyof typeof TRADE_MANAGEMENT_EVENT_TYPE];

/**
 * One post-entry management event.
 */
export interface TradeManagementEvent {
  /**
   * Unique event identifier.
   */
  eventId: string;

  /**
   * Event timestamp (ISO 8601).
   */
  timestamp: string;

  /**
   * Management event type.
   */
  type: TradeManagementEventType;

  /**
   * Updated stop price.
   * Required only for STOP_MOVED.
   */
  newStopPrice?: number;

  /**
   * Signed quantity change.
   * Positive = Scale In
   * Negative = Scale Out / Partial Exit
   */
  quantityChange?: number;

  /**
   * Execution price.
   */
  price?: number;

  /**
   * Reason for management action.
   */
  reason: string;

  /**
   * Emotional state.
   * Scale: 1–10
   */
  emotion: number;

  /**
   * Confidence.
   * Scale: 1–10
   */
  confidence: number;
}

/**
 * Complete Trade Management section.
 *
 * Represents every change made after
 * the trade becomes Active.
 */
export interface TradeManagement {
  events: TradeManagementEvent[];
}
