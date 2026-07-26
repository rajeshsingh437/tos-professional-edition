/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Factory
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.004
 * ============================================================
 */

import { EXIT_REASON_CATEGORY } from "../trade.exit";

import { INSTRUMENT_TYPE, type TradeInstrument } from "../trade.instrument";

import { TIMEFRAME } from "../trade.planning";

import { TRADE_EMOTION } from "../trade.psychology";

import { READINESS_VERDICT } from "../trade.readiness";

import { TRADE_STATUS } from "../trade.status";

import type { Trade } from "../trade.types";

/**
 * Optional values supplied when creating a Trade.
 */
export interface CreateTradeOptions {
  createdBy?: string;
  source?: string;
}

/**
 * Creates an empty TradeInstrument.
 */
function createEmptyInstrument(): TradeInstrument {
  return {
    symbol: "",
    instrumentType: INSTRUMENT_TYPE.INDEX,
    strikePrice: 0,
    expiryDate: "",
    lotSize: 0,
    contractMultiplier: 1,
  };
}

/**
 * Creates an empty Trade.
 */
export function createEmptyTrade(options: CreateTradeOptions = {}): Trade {
  const now = new Date().toISOString();

  return {
    metadata: {
      schemaVersion: "1.1",
      createdAt: now,
      updatedAt: now,
      createdBy: options.createdBy ?? "system",
      modifiedBy: options.createdBy ?? "system",
      source: options.source ?? "manual",
      archived: false,
      deleted: false,
    },

    identity: {
      tradeId: crypto.randomUUID(),
      createdDate: now,
      createdBy: options.createdBy ?? "system",
      status: TRADE_STATUS.DRAFT,
      version: 1,
      tags: [],
      lifecycleHistory: [],
    },

    instrument: createEmptyInstrument(),

    planning: {
      instrument: createEmptyInstrument(),
      whyThisTrade: "",
      edge: "",
      strategy: "",
      timeframe: TIMEFRAME.INTRADAY,
      expectedRiskReward: 0,
      maximumRisk: 0,
      maximumLoss: 0,
      positionSize: 0,
      capitalAllocation: 0,
      invalidation: "",
      entryTrigger: "",
    },

    readiness: {
      checklist: [],
      todaysMindset: "",
      revengeTradingFlag: false,
      score: 0,
      verdict: READINESS_VERDICT.STOP,
    },

    execution: {
      entries: [],
      averageEntry: 0,
      slippage: 0,
      broker: "",
    },

    management: {
      events: [],
    },

    exit: {
      exits: [],
      averageExit: 0,
      realisedPnL: 0,
      rMultiple: 0,
      exitReasonCategory: EXIT_REASON_CATEGORY.OTHER,
    },

    review: {
      planFollowed: false,
      disciplineMaintained: false,
      sizingCorrect: false,
      didInterfere: false,
      exitWasEmotional: false,
      stopRespected: false,
      wouldTakeAgain: false,
      processScore: 0,
    },

    psychology: {
      emotionBefore: TRADE_EMOTION.NEUTRAL,
      emotionDuring: TRADE_EMOTION.NEUTRAL,
      emotionAfter: TRADE_EMOTION.NEUTRAL,
      confidence: 0,
      stress: 0,
      fear: 0,
      greed: 0,
      patience: 0,
      distraction: 0,
    },

    learning: {
      lessonLearned: "",
    },

    attachments: {
      attachments: [],
    },
  };
}

/**
 * Creates a new draft Trade.
 */
export function createDraftTrade(options: CreateTradeOptions = {}): Trade {
  return createEmptyTrade(options);
}

/**
 * Creates a deep copy of a Trade.
 */
export function cloneTrade(trade: Trade): Trade {
  return structuredClone(trade);
}

/**
 * Creates a Trade from an existing template.
 */
export function createTradeFromTemplate(template: Trade): Trade {
  return cloneTrade(template);
}
