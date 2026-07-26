/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Validation Rules
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.004
 * ============================================================
 */

import type { Trade } from "../trade.types";

import {
  VALIDATION_SEVERITY,
  type ValidationMessage,
} from "./trade.validation.types";

/**
 * Validate the Planning section.
 */
export function validatePlanning(trade: Trade): ValidationMessage[] {
  const messages: ValidationMessage[] = [];

  if (trade.planning.whyThisTrade.trim() === "") {
    messages.push({
      code: "PLANNING_REASON_REQUIRED",
      field: "planning.whyThisTrade",
      message: "Reason for taking the trade is required.",
      severity: VALIDATION_SEVERITY.ERROR,
    });
  }

  if (trade.planning.edge.trim() === "") {
    messages.push({
      code: "PLANNING_EDGE_REQUIRED",
      field: "planning.edge",
      message: "Trading edge must be defined.",
      severity: VALIDATION_SEVERITY.ERROR,
    });
  }

  if (trade.planning.strategy.trim() === "") {
    messages.push({
      code: "PLANNING_STRATEGY_REQUIRED",
      field: "planning.strategy",
      message: "Trading strategy must be specified.",
      severity: VALIDATION_SEVERITY.ERROR,
    });
  }

  if (trade.planning.entryTrigger.trim() === "") {
    messages.push({
      code: "PLANNING_ENTRY_TRIGGER_REQUIRED",
      field: "planning.entryTrigger",
      message: "Entry trigger is required.",
      severity: VALIDATION_SEVERITY.ERROR,
    });
  }

  if (trade.planning.invalidation.trim() === "") {
    messages.push({
      code: "PLANNING_INVALIDATION_REQUIRED",
      field: "planning.invalidation",
      message: "Invalidation condition is required.",
      severity: VALIDATION_SEVERITY.ERROR,
    });
  }

  return messages;
}

/**
 * Validate the Instrument section.
 */
export function validateInstrument(trade: Trade): ValidationMessage[] {
  const messages: ValidationMessage[] = [];

  if (trade.instrument.symbol.trim() === "") {
    messages.push({
      code: "INSTRUMENT_SYMBOL_REQUIRED",
      field: "instrument.symbol",
      message: "Trading symbol is required.",
      severity: VALIDATION_SEVERITY.ERROR,
    });
  }

  return messages;
}

/**
 * Validate the Readiness section.
 */
export function validateReadiness(trade: Trade): ValidationMessage[] {
  const messages: ValidationMessage[] = [];

  if (trade.readiness.checklist.length === 0) {
    messages.push({
      code: "READINESS_CHECKLIST_EMPTY",
      field: "readiness.checklist",
      message: "Readiness checklist has not been completed.",
      severity: VALIDATION_SEVERITY.WARNING,
    });
  }

  return messages;
}

/**
 * Validate the Review section.
 */
export function validateReview(trade: Trade): ValidationMessage[] {
  const messages: ValidationMessage[] = [];

  if (trade.review.processScore < 0 || trade.review.processScore > 100) {
    messages.push({
      code: "PROCESS_SCORE_INVALID",
      field: "review.processScore",
      message: "Process Score must be between 0 and 100.",
      severity: VALIDATION_SEVERITY.ERROR,
    });
  }

  return messages;
}
