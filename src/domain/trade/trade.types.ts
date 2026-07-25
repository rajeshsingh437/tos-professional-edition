/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Root Trade Object
 *
 * Purpose:
 * Aggregates all domain interfaces into a single Trade object.
 * ============================================================
 */

import type { TradeAttachments } from "./trade.attachments";
import type { TradeExecution } from "./trade.execution";
import type { TradeExit } from "./trade.exit";
import type { TradeIdentity } from "./trade.identity";
import type { TradeLearning } from "./trade.learning";
import type { TradeManagement } from "./trade.management";
import type { TradeMetadata } from "./trade.metadata";
import type { TradePlanning } from "./trade.planning";
import type { TradePsychology } from "./trade.psychology";
import type { TradeReadiness } from "./trade.readiness";
import type { TradeReview } from "./trade.review";
/**
 * Root Trade object.
 */
export interface Trade {
  identity: TradeIdentity;

  planning: TradePlanning;

  readiness: TradeReadiness;

  execution: TradeExecution;

  management: TradeManagement;

  exit: TradeExit;

  review: TradeReview;

  psychology: TradePsychology;

  learning: TradeLearning;

  attachments: TradeAttachments;
}
export interface Trade {
  metadata: TradeMetadata;

  identity: TradeIdentity;

  planning: TradePlanning;

  readiness: TradeReadiness;

  execution: TradeExecution;

  management: TradeManagement;

  exit: TradeExit;

  review: TradeReview;

  psychology: TradePsychology;

  learning: TradeLearning;

  attachments: TradeAttachments;
}
