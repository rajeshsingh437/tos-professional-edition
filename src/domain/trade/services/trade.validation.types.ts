/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Validation Types
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.004
 * ============================================================
 */

/**
 * Validation severity levels.
 */
export const VALIDATION_SEVERITY = {
  ERROR: "ERROR",
  WARNING: "WARNING",
  INFO: "INFO",
} as const;

export type ValidationSeverity =
  (typeof VALIDATION_SEVERITY)[keyof typeof VALIDATION_SEVERITY];

/**
 * One validation message.
 */
export interface ValidationMessage {
  /**
   * Stable machine-readable code.
   *
   * Example:
   * PLANNING_EDGE_REQUIRED
   */
  code: string;

  /**
   * Object path.
   *
   * Example:
   * planning.edge
   */
  field: string;

  /**
   * Human-readable explanation.
   */
  message: string;

  /**
   * Message severity.
   */
  severity: ValidationSeverity;
}

/**
 * Complete validation result.
 */
export interface ValidationResult {
  /**
   * Overall result.
   */
  valid: boolean;

  /**
   * Overall completeness / quality score.
   * Range: 0–100.
   */
  score: number;

  /**
   * Validation errors.
   */
  errors: ValidationMessage[];

  /**
   * Non-blocking warnings.
   */
  warnings: ValidationMessage[];

  /**
   * Informational messages.
   */
  information: ValidationMessage[];
}
