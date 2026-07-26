/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Psychology
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

/**
 * Controlled emotion labels.
 */
export const TRADE_EMOTION = {
  CALM: "Calm",
  CONFIDENT: "Confident",
  ANXIOUS: "Anxious",
  FRUSTRATED: "Frustrated",
  EUPHORIC: "Euphoric",
  FEARFUL: "Fearful",
  NEUTRAL: "Neutral",
} as const;

export type TradeEmotion = (typeof TRADE_EMOTION)[keyof typeof TRADE_EMOTION];

/**
 * Trade Psychology
 *
 * Captures the trader's emotional state
 * before, during and after the trade.
 */
export interface TradePsychology {
  /**
   * Emotional state before entry.
   */
  emotionBefore: TradeEmotion;

  /**
   * Emotional state during the trade.
   */
  emotionDuring: TradeEmotion;

  /**
   * Emotional state after exit.
   */
  emotionAfter: TradeEmotion;

  /**
   * Confidence level.
   * Scale: 1–10
   */
  confidence: number;

  /**
   * Stress level.
   * Scale: 1–10
   */
  stress: number;

  /**
   * Fear level.
   * Scale: 1–10
   */
  fear: number;

  /**
   * Greed level.
   * Scale: 1–10
   */
  greed: number;

  /**
   * Patience level.
   * Scale: 1–10
   */
  patience: number;

  /**
   * Distraction level.
   * Scale: 1–10
   */
  distraction: number;
}
