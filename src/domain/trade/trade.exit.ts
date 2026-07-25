/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Exit
 *
 * Purpose:
 * Captures how the trade was closed and its financial outcome.
 * ============================================================
 */

/**
 * Trade Exit
 */
export interface TradeExit {
  /**
   * Exit price.
   */
  exitPrice: number;

  /**
   * Exit date & time (ISO 8601).
   */
  exitTime: string;

  /**
   * Quantity exited.
   */
  exitQuantity: number;

  /**
   * Exit reason.
   */
  exitReason: string;

  /**
   * Gross profit or loss.
   */
  grossPnL: number;

  /**
   * Net profit or loss.
   */
  netPnL: number;

  /**
   * Fees, brokerage and taxes.
   */
  transactionCost: number;

  /**
   * Return as percentage.
   */
  returnPercentage: number;

  /**
   * Planned exit followed?
   */
  plannedExitFollowed: boolean;

  /**
   * Additional exit notes.
   */
  notes: string;
}
