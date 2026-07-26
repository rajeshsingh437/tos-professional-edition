/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Shared Primitive Types
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.004
 * ============================================================
 */

/**
 * Unique identifiers.
 */
export type TradeId = string;
export type RuleId = string;
export type EventId = string;
export type UserId = string;

/**
 * ISO 8601 date representations.
 *
 * Examples:
 * 2026-07-26
 * 2026-07-26T09:15:30Z
 */
export type ISODate = string;
export type ISODateTime = string;

/**
 * Financial values.
 */
export type Money = number;
export type Price = number;
export type Quantity = number;
export type LotCount = number;
export type Percentage = number;
export type Score = number;
export type RiskMultiple = number;

/**
 * Generic text aliases.
 */
export type Notes = string;
export type Reason = string;
export type Url = string;
