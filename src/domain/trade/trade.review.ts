/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Review
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

/**
 * Trade Review
 *
 * Evaluates the quality of execution
 * independently of financial outcome.
 */
export interface TradeReview {
  /**
   * Was the planned entry followed?
   */
  planFollowed: boolean;

  /**
   * Was discipline maintained?
   */
  disciplineMaintained: boolean;

  /**
   * Was the planned position size used?
   */
  sizingCorrect: boolean;

  /**
   * Did the trader interfere manually?
   */
  didInterfere: boolean;

  /**
   * Was the exit emotionally driven?
   */
  exitWasEmotional: boolean;

  /**
   * Was the stop respected?
   */
  stopRespected: boolean;

  /**
   * Would this exact trade be taken again?
   */
  wouldTakeAgain: boolean;

  /**
   * Computed process score.
   * Range: 0–100
   */
  processScore: number;
}
