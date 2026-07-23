import type {
  DisciplineMetric,
  DisciplineSessionData,
} from "../constants/disciplineData";

export type DisciplineGrade = "A+" | "A" | "B" | "C" | "D";
export type DisciplineStatus = "EXCELLENT" | "GOOD" | "ATTENTION" | "LOCKED";

export interface DisciplineFlag {
  metric: DisciplineMetric;
  severity: "warning" | "breach";
}

export interface DisciplineResult {
  score: number;
  grade: DisciplineGrade;
  status: DisciplineStatus;
  recommendation: string;
  tradingLocked: boolean;
  flags: DisciplineFlag[];
}

function isMetricSatisfied(metric: DisciplineMetric) {
  return metric.status === "met";
}

function getGrade(score: number): DisciplineGrade {
  if (score >= 96) return "A+";
  if (score >= 90) return "A";
  if (score >= 80) return "B";
  if (score >= 70) return "C";
  return "D";
}

function getRecommendation(
  score: number,
  tradingLocked: boolean,
): string {
  if (tradingLocked) {
    return "Trading is locked: respect the daily stop and review the session.";
  }

  if (score >= 96) {
    return "Excellent discipline. Continue following your process.";
  }

  if (score >= 80) {
    return "Solid discipline. Complete the journal and review exit execution.";
  }

  if (score >= 70) {
    return "Slow down and reduce risk until the open discipline items are resolved.";
  }

  return "Stop trading for today and complete a structured review before tomorrow.";
}

export function calculateDiscipline(
  session: DisciplineSessionData,
): DisciplineResult {
  const totalWeight = session.metrics.reduce(
    (sum, metric) => sum + metric.weight,
    0,
  );

  const earnedWeight = session.metrics.reduce(
    (sum, metric) =>
      isMetricSatisfied(metric) ? sum + metric.weight : sum,
    0,
  );

  const score = totalWeight === 0 ? 0 : Math.round((earnedWeight / totalWeight) * 100);
  const dailyStopBreached = session.metrics.some(
    (metric) => metric.id === "daily-stop" && metric.status === "breach",
  );
  const tradingLocked = dailyStopBreached || session.stopViolationCount > 0;
  const flags = session.metrics
    .filter(
      (
        metric,
      ): metric is DisciplineMetric & { status: "warning" | "breach" } =>
        metric.status !== "met",
    )
    .map((metric) => ({
      metric,
      severity: metric.status,
    }));

  const status: DisciplineStatus = tradingLocked
    ? "LOCKED"
    : score >= 90
      ? "EXCELLENT"
      : score >= 80
        ? "GOOD"
        : "ATTENTION";

  return {
    score,
    grade: getGrade(score),
    status,
    recommendation: getRecommendation(score, tradingLocked),
    tradingLocked,
    flags,
  };
}
