export interface TradeMetadata {
  schemaVersion: number;

  createdAt: string;

  updatedAt: string;

  createdBy: string;

  modifiedBy: string;

  source: "manual" | "import" | "broker" | "api";

  archived: boolean;

  archivedAt: string | null;

  deleted: boolean;
}
