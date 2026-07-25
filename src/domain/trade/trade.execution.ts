/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Execution
 *
 * Purpose:
 * Records what actually happened when the trade was executed.
 * ============================================================
 */

/**
 * Trade Execution
 */
export interface TradeExecution {
  /**
   * Planned entry price.
   */
  plannedEntryPrice: number;

  /**
   * Actual entry price.
   */
  actualEntryPrice: number;

  /**
   * Initial stop loss.
   */
  stopLoss: number;

  /**
   * Planned target price.
   */
  targetPrice: number;

  /**
   * Quantity executed.
   */
  quantity: number;

  /**
   * Time when order was executed.
   */
  executionTime: string;

  /**
   * Broker order reference.
   */
  orderId: string;

  /**
   * Order type.
   */
  orderType: string;

  /**
   * Whether slippage occurred.
   */
  slippageOccurred: boolean;

  /**
   * Slippage value.
   */
  slippage: number;

  /**
   * Execution notes.
   */
  notes: string;
}
