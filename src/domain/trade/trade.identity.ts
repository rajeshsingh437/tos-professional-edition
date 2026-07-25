/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Identity
 *
 * Purpose:
 * Defines the permanent identity of a trade.
 *
 * One Trade = One Trade ID.
 *
 * The identity of a trade never changes throughout its lifecycle.
 * ============================================================
 */

import type { TradeStatus } from "./trade.status";

/**
 * Permanent identity of a Trade.
 */
export interface TradeIdentity {
  /**
   * Unique identifier for the trade.
   * Generated once when the trade is created.
   * Never changes.
   */
  tradeId: string;

  /**
   * Date and time when the trade was created.
   */
  createdDate: Date;

  /**
   * User who created the trade.
   */
  createdBy: string;

  /**
   * Current lifecycle status.
   */
  status: TradeStatus;

  /**
   * Version number of the trade.
   * Starts at 1.
   */
  version: number;

  /**
   * Optional labels used for filtering and reporting.
   */
  tags: string[];
}
