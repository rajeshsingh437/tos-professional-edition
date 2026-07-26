/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Instrument
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

/**
 * Instrument category.
 */
export const INSTRUMENT_TYPE = {
  INDEX: "INDEX",
  STOCK: "STOCK",
} as const;

export type InstrumentType =
  (typeof INSTRUMENT_TYPE)[keyof typeof INSTRUMENT_TYPE];

/**
 * Option contract type.
 */
export const OPTION_TYPE = {
  CE: "CE",
  PE: "PE",
} as const;

export type OptionType = (typeof OPTION_TYPE)[keyof typeof OPTION_TYPE];

/**
 * Instrument being traded.
 */
export interface TradeInstrument {
  /**
   * Trading symbol.
   * Example: NIFTY
   */
  symbol: string;

  /**
   * INDEX or STOCK.
   */
  instrumentType: InstrumentType;

  /**
   * CE or PE.
   *
   * Optional because non-option instruments
   * (future versions such as cash equity)
   * won't use it.
   */
  optionType?: OptionType;

  /**
   * Strike price.
   */
  strikePrice: number;

  /**
   * Expiry date (ISO 8601).
   */
  expiryDate: string;

  /**
   * Exchange lot size.
   */
  lotSize: number;

  /**
   * Contract multiplier.
   * Usually 1.
   */
  contractMultiplier: number;
}
