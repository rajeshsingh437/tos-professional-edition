import type { ChecklistItem } from "../constants/sessionChecklist";

export interface ReadinessResult {
  score: number;
  status: "GO" | "CAUTION" | "STOP";
  recommendation: string;
}

export function calculateReadiness(
  checklist: ChecklistItem[],
): ReadinessResult {
  const totalWeight = checklist.reduce((sum, item) => sum + item.weight, 0);

  const completedWeight = checklist.reduce(
    (sum, item) => (item.completed ? sum + item.weight : sum),
    0,
  );

  const score = Math.round((completedWeight / totalWeight) * 100);

  let status: "GO" | "CAUTION" | "STOP";
  let recommendation = "";

  if (score >= 90) {
    status = "GO";
    recommendation = "Proceed with your planned position size.";
  } else if (score >= 70) {
    status = "CAUTION";
    recommendation = "Reduce risk until all checklist items are complete.";
  } else {
    status = "STOP";
    recommendation = "Complete your preparation before trading.";
  }

  return {
    score,
    status,
    recommendation,
  };
}
