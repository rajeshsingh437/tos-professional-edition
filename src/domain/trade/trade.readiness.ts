/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Readiness
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

/**
 * Individual readiness checklist item.
 */
export interface ReadinessChecklistItem {
  /**
   * Checklist label.
   */
  label: string;

  /**
   * Weight.
   * Total across one checklist = 100.
   */
  weight: number;

  /**
   * Whether this condition passed.
   */
  passed: boolean;
}

/**
 * GO / CAUTION / STOP verdict.
 */
export const READINESS_VERDICT = {
  GO: "GO",
  CAUTION: "CAUTION",
  STOP: "STOP",
} as const;

export type ReadinessVerdict =
  (typeof READINESS_VERDICT)[keyof typeof READINESS_VERDICT];

/**
 * Readiness section.
 *
 * Determines whether the trade
 * should be executed.
 */
export interface TradeReadiness {
  /**
   * Weighted checklist.
   */
  checklist: ReadinessChecklistItem[];

  /**
   * Optional notes about today's mindset.
   */
  todaysMindset?: string;

  /**
   * Revenge trading override.
   */
  revengeTradingFlag: boolean;

  /**
   * Computed score.
   * Range: 0–100.
   */
  score: number;

  /**
   * Computed verdict.
   */
  verdict: ReadinessVerdict;
}
