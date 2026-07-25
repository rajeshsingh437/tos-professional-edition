/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Learning
 *
 * Purpose:
 * Records lessons and improvements from each trade.
 * ============================================================
 */

export interface TradeLearning {
  /**
   * Primary lesson learned.
   */
  primaryLesson: string;

  /**
   * What worked well?
   */
  strengths: string[];

  /**
   * What needs improvement?
   */
  improvements: string[];

  /**
   * Mistakes identified.
   */
  mistakes: string[];

  /**
   * Action items for future trades.
   */
  actionItems: string[];

  /**
   * Tags for later analysis.
   */
  tags: string[];

  /**
   * Personal notes.
   */
  notes: string;
}
