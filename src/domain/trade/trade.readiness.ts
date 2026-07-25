/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Readiness
 *
 * Purpose:
 * Defines whether the trader is ready to execute the plan.
 * ============================================================
 */

/**
 * Trade Readiness Checklist
 */
export interface TradeReadiness {
  sleepAdequate: boolean;

  emotionStable: boolean;

  newsChecked: boolean;

  economicCalendarChecked: boolean;

  trendConfirmed: boolean;

  liquidityAdequate: boolean;

  riskRewardAcceptable: boolean;

  riskWithinDailyLimit: boolean;

  todaysMindset: string;

  revengeTrading: boolean;
}
