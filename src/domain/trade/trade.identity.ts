/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Identity
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

import type { TradeStatus } from "./trade.status";

/**
 * Records every lifecycle transition.
 */
export interface LifecycleHistoryEntry {
  /**
   * Lifecycle status at this point in time.
   */
  status: TradeStatus;

  /**
   * ISO 8601 timestamp.
   */
  timestamp: string;
}

/**
 * Permanent identity of a Trade.
 */
export interface TradeIdentity {
  /**
   * Immutable unique Trade ID.
   * Example:
   * TOS-20260726-0001
   */
  tradeId: string;

  /**
   * ISO 8601 timestamp.
   * Must match the first lifecycle history timestamp.
   */
  createdDate: string;

  /**
   * User who created this trade.
   */
  createdBy: string;

  /**
   * Current lifecycle status.
   *
   * NOTE:
   * During validation this should always equal
   * lifecycleHistory[last].status.
   */
  status: TradeStatus;

  /**
   * Incremented on every edit.
   */
  version: number;

  /**
   * Optional searchable labels.
   */
  tags: string[];

  /**
   * Complete lifecycle history.
   */
  lifecycleHistory: LifecycleHistoryEntry[];
}
