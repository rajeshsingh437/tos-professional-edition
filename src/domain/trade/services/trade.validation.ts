/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Validation Engine
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.004
 * ============================================================
 */

import type { Trade } from "../trade.types";

import {
  validateInstrument,
  validatePlanning,
  validateReadiness,
  validateReview,
} from "./trade.validation.rules";

import {
  VALIDATION_SEVERITY,
  type ValidationMessage,
  type ValidationResult,
} from "./trade.validation.types";

/**
 * Calculates an overall validation score.
 *
 * Starts at 100 and deducts:
 * -10 for each ERROR
 * -2 for each WARNING
 *
 * Minimum score = 0.
 */
function calculateValidationScore(messages: ValidationMessage[]): number {
  let score = 100;

  for (const message of messages) {
    switch (message.severity) {
      case VALIDATION_SEVERITY.ERROR:
        score -= 10;
        break;

      case VALIDATION_SEVERITY.WARNING:
        score -= 2;
        break;

      default:
        break;
    }
  }

  return Math.max(0, score);
}

/**
 * Validates an entire Trade object.
 */
export function validateTrade(trade: Trade): ValidationResult {
  const messages: ValidationMessage[] = [
    ...validateInstrument(trade),
    ...validatePlanning(trade),
    ...validateReadiness(trade),
    ...validateReview(trade),
  ];

  const errors = messages.filter(
    (m) => m.severity === VALIDATION_SEVERITY.ERROR,
  );

  const warnings = messages.filter(
    (m) => m.severity === VALIDATION_SEVERITY.WARNING,
  );

  const information = messages.filter(
    (m) => m.severity === VALIDATION_SEVERITY.INFO,
  );

  return {
    valid: errors.length === 0,
    score: calculateValidationScore(messages),
    errors,
    warnings,
    information,
  };
}
