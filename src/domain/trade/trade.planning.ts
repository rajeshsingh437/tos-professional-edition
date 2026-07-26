/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Planning
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

import type { TradeInstrument } from "./trade.instrument";

/**
 * Trading timeframe.
 */
export const TIMEFRAME = {
  INTRADAY: "Intraday",
  SWING: "Swing",
  POSITIONAL: "Positional",
} as const;

export type Timeframe = (typeof TIMEFRAME)[keyof typeof TIMEFRAME];

/**
 * Planning section.
 *
 * This represents the official trading plan and
 * must be completed before a trade can move beyond
 * the Draft stage.
 */
export interface TradePlanning {
  /**
   * Reference to the traded instrument.
   */
  instrument: TradeInstrument;

  /**
   * Why should this trade exist?
   */
  whyThisTrade: string;

  /**
   * The repeatable statistical edge.
   */
  edge: string;

  /**
   * Named trading setup.
   * Example:
   * ORB Breakout
   * VWAP Reversal
   */
  strategy: string;

  /**
   * Trading timeframe.
   */
  timeframe: Timeframe;

  /**
   * Expected Reward : Risk.
   * Example:
   * 2.0
   */
  expectedRiskReward: number;

  /**
   * Planned maximum risk.
   * INR.
   */
  maximumRisk: number;

  /**
   * Worst possible loss.
   * INR.
   */
  maximumLoss: number;

  /**
   * Planned position size.
   * Number of lots.
   */
  positionSize: number;

  /**
   * Planned capital allocation.
   * INR.
   */
  capitalAllocation: number;

  /**
   * Optional market context.
   */
  marketContext?: string;

  /**
   * Optional supporting thesis.
   */
  supportingThesis?: string;

  /**
   * What proves this trade wrong?
   */
  invalidation: string;

  /**
   * Observable trigger for entry.
   */
  entryTrigger: string;
}
