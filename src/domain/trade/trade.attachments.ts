/**
 * ============================================================
 * TOS Professional Edition
 * Trade Lifecycle Engine (TLE)
 * ------------------------------------------------------------
 * Trade Attachments
 *
 * Purpose:
 * References all external artefacts linked to a trade.
 * ============================================================
 */

/**
 * Single attachment.
 */
export interface TradeAttachment {
  /**
   * Unique attachment ID.
   */
  id: string;

  /**
   * File name.
   */
  fileName: string;

  /**
   * File type.
   */
  fileType: string;

  /**
   * Local path or URL.
   */
  filePath: string;

  /**
   * Optional description.
   */
  description: string;

  /**
   * Upload timestamp (ISO 8601).
   */
  uploadedAt: string;
}

/**
 * Attachment collection.
 */
export interface TradeAttachments {
  attachments: TradeAttachment[];
}
