/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Psychology
 *
 * Purpose:
 * Captures the trader's emotional and psychological state.
 * ============================================================
 */

export interface TradePsychology {
  /**
   * Confidence before entering the trade (0–10).
   */
  confidenceLevel: number;

  /**
   * Stress level during the trade (0–10).
   */
  stressLevel: number;

  /**
   * Emotional state before entry.
   */
  emotionBeforeTrade: string;

  /**
   * Emotional state after exit.
   */
  emotionAfterTrade: string;

  /**
   * Was the plan followed?
   */
  disciplineMaintained: boolean;

  /**
   * Was there any FOMO?
   */
  experiencedFOMO: boolean;

  /**
   * Was there hesitation?
   */
  hesitationObserved: boolean;

  /**
   * Was there overconfidence?
   */
  overconfidenceObserved: boolean;

  /**
   * Any signs of revenge trading?
   */
  revengeTradingObserved: boolean;

  /**
   * Psychology notes.
   */
  notes: string;
}
