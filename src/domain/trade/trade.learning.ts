/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Learning
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

/**
 * Reference to a trading rule.
 */
export interface TradeRuleReference {
  /**
   * Unique rule identifier.
   */
  ruleId: string;

  /**
   * Human-readable rule label.
   */
  label: string;
}

/**
 * Trade Learning
 *
 * Every trade should leave behind
 * something that improves future trading.
 */
export interface TradeLearning {
  /**
   * Biggest mistake made.
   */
  biggestMistake?: string;

  /**
   * Biggest success.
   */
  biggestSuccess?: string;

  /**
   * Primary lesson learned.
   */
  lessonLearned: string;

  /**
   * Rule created because of this trade.
   */
  ruleCreated?: TradeRuleReference;

  /**
   * Rule broken during this trade.
   */
  ruleBroken?: TradeRuleReference;
}
