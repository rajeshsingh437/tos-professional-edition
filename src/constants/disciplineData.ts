export type DisciplineMetricStatus = "met" | "warning" | "breach";

export interface DisciplineMetric {
  id:
    | "daily-stop"
    | "position-sizing"
    | "checklist"
    | "revenge-trading"
    | "journal"
    | "screenshot"
    | "emotional-trading"
    | "exit-execution";
  title: string;
  detail: string;
  weight: number;
  status: DisciplineMetricStatus;
}

export interface DisciplineSessionData {
  metrics: DisciplineMetric[];
  stopViolationCount: number;
  impulseReentryCount: number;
  earlyExitCount: number;
  ruleOverrideCount: number;
}

export const disciplineSessionData: DisciplineSessionData = {
  metrics: [
    {
      id: "daily-stop",
      title: "Daily stop respected",
      detail: "No daily-loss limit breach",
      weight: 20,
      status: "met",
    },
    {
      id: "position-sizing",
      title: "Position sizing respected",
      detail: "All entries stayed within plan",
      weight: 20,
      status: "met",
    },
    {
      id: "checklist",
      title: "Pre-trade checklist completed",
      detail: "Every trade was validated first",
      weight: 15,
      status: "met",
    },
    {
      id: "revenge-trading",
      title: "No revenge trading",
      detail: "No emotion-led re-entry detected",
      weight: 15,
      status: "met",
    },
    {
      id: "journal",
      title: "Journal completed",
      detail: "Complete the post-session review",
      weight: 10,
      status: "warning",
    },
    {
      id: "screenshot",
      title: "Screenshot attached",
      detail: "Attach a chart to the trade review",
      weight: 5,
      status: "warning",
    },
    {
      id: "emotional-trading",
      title: "No emotional trading",
      detail: "Maintain calm, planned execution",
      weight: 10,
      status: "met",
    },
    {
      id: "exit-execution",
      title: "Exit plan followed",
      detail: "One early exit needs review",
      weight: 5,
      status: "warning",
    },
  ],
  stopViolationCount: 0,
  impulseReentryCount: 0,
  earlyExitCount: 1,
  ruleOverrideCount: 0,
};
