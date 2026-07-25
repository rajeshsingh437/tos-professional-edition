/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Review
 *
 * Purpose:
 * Post-trade evaluation of execution, outcome and learning.
 * ============================================================
 */

/**
 * Trade Review
 */
export interface TradeReview {
  /**
   * Was this a good trade idea?
   */
  goodIdea: boolean;

  /**
   * Was the execution disciplined?
   */
  executedWell: boolean;

  /**
   * Was something valuable learned?
   */
  learnedSomething: boolean;

  /**
   * Process score (0–100).
   */
  processScore: number;

  /**
   * Outcome score (0–100).
   */
  outcomeScore: number;

  /**
   * Biggest mistake made.
   */
  biggestMistake: string;

  /**
   * Biggest strength shown.
   */
  biggestStrength: string;

  /**
   * Key lesson from this trade.
   */
  keyLesson: string;

  /**
   * Action for future improvement.
   */
  improvementAction: string;

  /**
   * Overall review notes.
   */
  reviewNotes: string;
}
