/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Execution
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

/**
 * Supported order types.
 */
export const ORDER_TYPE = {
  MARKET: "MARKET",
  LIMIT: "LIMIT",
  STOP: "STOP",
  STOP_LIMIT: "STOP_LIMIT",
} as const;

export type OrderType = (typeof ORDER_TYPE)[keyof typeof ORDER_TYPE];

/**
 * One executed entry leg.
 */
export interface ExecutionLeg {
  /**
   * Unique leg identifier.
   */
  legId: string;

  /**
   * Executed price.
   */
  price: number;

  /**
   * Quantity executed.
   */
  quantity: number;

  /**
   * Execution timestamp (ISO 8601).
   */
  timestamp: string;

  /**
   * Order type.
   */
  orderType: OrderType;
}

/**
 * Execution section.
 *
 * Contains every execution that forms
 * the ORIGINAL planned position.
 */
export interface TradeExecution {
  /**
   * Original entry legs.
   */
  entries: ExecutionLeg[];

  /**
   * Quantity-weighted average entry.
   * Computed.
   */
  averageEntry: number;

  /**
   * Total slippage.
   * INR.
   */
  slippage: number;

  /**
   * Broker used.
   */
  broker: string;

  /**
   * Optional execution notes.
   */
  executionNotes?: string;
}
