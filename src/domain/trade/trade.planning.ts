/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Planning
 *
 * Purpose:
 * Defines the trading plan before any order is placed.
 * ============================================================
 */

/**
 * Trading Plan
 */
export interface TradePlanning {
  /**
   * Why this trade?
   */
  tradeReason: string;

  /**
   * Trading edge.
   */
  edge: string;

  /**
   * Trading strategy.
   */
  strategy: string;

  /**
   * Trading timeframe.
   */
  timeframe: string;

  /**
   * Expected Risk : Reward ratio.
   */
  expectedRiskReward: number;

  /**
   * Maximum acceptable risk.
   */
  maximumRisk: number;

  /**
   * Maximum acceptable loss.
   */
  maximumLoss: number;

  /**
   * Position size.
   */
  positionSize: number;

  /**
   * Capital allocated.
   */
  capitalAllocation: number;

  /**
   * Current market context.
   */
  marketContext: string;

  /**
   * Supporting thesis.
   */
  supportingThesis: string;

  /**
   * Trade invalidation.
   */
  invalidation: string;

  /**
   * Entry trigger.
   */
  entryTrigger: string;
}
