/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Aggregate
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.004
 * ============================================================
 */

import type { TradeAttachments } from "./trade.attachments";
import type { TradeExecution } from "./trade.execution";
import type { TradeExit } from "./trade.exit";
import type { TradeIdentity } from "./trade.identity";
import type { TradeInstrument } from "./trade.instrument";
import type { TradeLearning } from "./trade.learning";
import type { TradeManagement } from "./trade.management";
import type { TradeMetadata } from "./trade.metadata";
import type { TradePlanning } from "./trade.planning";
import type { TradePsychology } from "./trade.psychology";
import type { TradeReadiness } from "./trade.readiness";
import type { TradeReview } from "./trade.review";

/**
 * Canonical Trade Aggregate.
 *
 * This interface represents one complete trade and acts as the
 * single source of truth throughout the application.
 */
export interface Trade {
  /**
   * Application metadata.
   */
  metadata: TradeMetadata;

  /**
   * Identity and lifecycle information.
   */
  identity: TradeIdentity;

  /**
   * Instrument being traded.
   */
  instrument: TradeInstrument;

  /**
   * Planning performed before entry.
   */
  planning: TradePlanning;

  /**
   * Readiness checklist and verdict.
   */
  readiness: TradeReadiness;

  /**
   * Entry execution details.
   */
  execution: TradeExecution;

  /**
   * Trade management events.
   */
  management: TradeManagement;

  /**
   * Exit information.
   */
  exit: TradeExit;

  /**
   * Post-trade review.
   */
  review: TradeReview;

  /**
   * Trader psychology observations.
   */
  psychology: TradePsychology;

  /**
   * Lessons learned.
   */
  learning: TradeLearning;

  /**
   * Screenshots and supporting evidence.
   */
  attachments: TradeAttachments;
}
