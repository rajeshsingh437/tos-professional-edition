/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Management
 *
 * Purpose:
 * Captures everything that happens while a trade is active.
 * ============================================================
 */

/**
 * Trade Management
 */
export interface TradeManagement {
  /**
   * Stop loss moved.
   */
  stopAdjusted: boolean;

  /**
   * New stop loss value.
   */
  adjustedStopLoss: number;

  /**
   * Partial exits taken.
   */
  partialExitTaken: boolean;

  /**
   * Quantity exited partially.
   */
  partialExitQuantity: number;

  /**
   * Current open quantity.
   */
  remainingQuantity: number;

  /**
   * Maximum favourable excursion.
   */
  mfe: number;

  /**
   * Maximum adverse excursion.
   */
  mae: number;

  /**
   * Highest unrealised profit.
   */
  peakUnrealisedProfit: number;

  /**
   * Lowest unrealised loss.
   */
  peakUnrealisedLoss: number;

  /**
   * Management notes.
   */
  notes: string;
}
