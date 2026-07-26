/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Exit
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

import type { OrderType } from "./trade.execution";

/**
 * Exit reason categories.
 */
export const EXIT_REASON_CATEGORY = {
  TARGET_HIT: "TARGET_HIT",
  STOP_HIT: "STOP_HIT",
  INVALIDATION: "INVALIDATION",
  TIME_STOP: "TIME_STOP",
  DISCRETIONARY: "DISCRETIONARY",
  OTHER: "OTHER",
} as const;

export type ExitReasonCategory =
  (typeof EXIT_REASON_CATEGORY)[keyof typeof EXIT_REASON_CATEGORY];

/**
 * One exit leg.
 */
export interface ExitLeg {
  /**
   * Unique leg identifier.
   */
  legId: string;

  /**
   * Executed exit price.
   */
  price: number;

  /**
   * Exit quantity.
   */
  quantity: number;

  /**
   * Exit timestamp (ISO 8601).
   */
  timestamp: string;

  /**
   * Order type.
   */
  orderType: OrderType;
}

/**
 * Trade Exit section.
 *
 * Represents every transaction that
 * closes the position.
 */
export interface TradeExit {
  /**
   * Exit legs.
   */
  exits: ExitLeg[];

  /**
   * Quantity-weighted average exit.
   * Computed.
   */
  averageExit: number;

  /**
   * Realised profit/loss (INR).
   * Computed.
   */
  realisedPnL: number;

  /**
   * Planned-risk multiple.
   * Computed.
   */
  rMultiple: number;

  /**
   * Exit category.
   */
  exitReasonCategory: ExitReasonCategory;

  /**
   * Optional notes.
   */
  exitReasonNote?: string;
}
