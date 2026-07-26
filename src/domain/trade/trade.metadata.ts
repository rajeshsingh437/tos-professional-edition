/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Metadata
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

export interface TradeMetadata {
  /**
   * Version of the Trade Object schema.
   * Example: "1.1"
   */
  schemaVersion: string;

  /**
   * Created timestamp (ISO 8601).
   */
  createdAt: string;

  /**
   * Last updated timestamp (ISO 8601).
   */
  updatedAt: string;

  /**
   * User who created the trade.
   */
  createdBy: string;

  /**
   * User who last modified the trade.
   */
  modifiedBy: string;

  /**
   * Source of trade creation.
   * Example:
   * MANUAL
   * IMPORT
   * BROKER_SYNC
   */
  source: string;

  /**
   * Archive flag.
   */
  archived: boolean;

  /**
   * Archive timestamp.
   */
  archivedAt?: string;

  /**
   * Soft delete flag.
   */
  deleted: boolean;
}
