/**
 * ============================================================
 * Trading Operating System (TOS)
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Module: Trade Attachments
 * Specification: TLE v1.1 (Frozen)
 * Build: 0.1.003
 * ============================================================
 */

/**
 * Trade stage at which evidence was captured.
 */
export const ATTACHMENT_STAGE = {
  BEFORE_ENTRY: "BeforeEntry",
  ENTRY: "Entry",
  MANAGEMENT: "Management",
  EXIT: "Exit",
  REVIEW: "Review",
} as const;

export type AttachmentStage =
  (typeof ATTACHMENT_STAGE)[keyof typeof ATTACHMENT_STAGE];

/**
 * Supported attachment types.
 */
export const ATTACHMENT_TYPE = {
  SCREENSHOT: "SCREENSHOT",
  VIDEO: "VIDEO",
  CHART_MARKUP: "CHART_MARKUP",
} as const;

export type AttachmentType =
  (typeof ATTACHMENT_TYPE)[keyof typeof ATTACHMENT_TYPE];

/**
 * One attachment associated with a trade.
 */
export interface TradeAttachment {
  /**
   * Stage when captured.
   */
  stage: AttachmentStage;

  /**
   * Attachment type.
   */
  type: AttachmentType;

  /**
   * File location.
   */
  url: string;

  /**
   * Capture timestamp.
   */
  timestamp: string;

  /**
   * Optional description.
   */
  caption?: string;
}

/**
 * Complete attachment collection.
 */
export interface TradeAttachments {
  attachments: TradeAttachment[];
}
