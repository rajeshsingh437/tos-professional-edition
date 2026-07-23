import { CheckCircle2, CircleAlert, LockKeyhole } from "lucide-react";

import Panel from "../common/Panel";
import ProgressBar from "../common/ProgressBar";

import { disciplineSessionData } from "../../constants/disciplineData";
import { calculateDiscipline } from "../../utils/disciplineEngine";

const statusClassNames = {
  EXCELLENT: "discipline-status-excellent",
  GOOD: "discipline-status-good",
  ATTENTION: "discipline-status-attention",
  LOCKED: "discipline-status-locked",
};

export default function DisciplineCenter() {
  const result = calculateDiscipline(disciplineSessionData);
  const coreMetrics = disciplineSessionData.metrics.slice(0, 4);
  const followUpMetrics = disciplineSessionData.metrics.slice(4);

  const renderMetric = (
    metric: (typeof disciplineSessionData.metrics)[number],
  ) => {
    const isMet = metric.status === "met";
    const Icon = isMet ? CheckCircle2 : CircleAlert;

    return (
      <div
        key={metric.id}
        className={`discipline-metric discipline-metric-${metric.status}`}
      >
        <Icon size={17} aria-hidden="true" />

        <div>
          <strong>{metric.title}</strong>
          <span>{metric.detail}</span>
        </div>

        <span className="discipline-weight">{metric.weight} pts</span>
      </div>
    );
  };

  return (
    <Panel
      title="Discipline Center"
      action={
        <span
          className={`discipline-status ${statusClassNames[result.status]}`}
        >
          {result.tradingLocked && <LockKeyhole size={14} />}
          {result.status}
        </span>
      }
    >
      <div className="discipline-center">
        <div className="discipline-score-row">
          <div>
            <p className="discipline-eyebrow">Today's discipline score</p>
            <strong className="discipline-score">{result.score}%</strong>
          </div>

          <div
            className="discipline-grade"
            aria-label={`Grade ${result.grade}`}
          >
            <span>GRADE</span>
            <strong>{result.grade}</strong>
          </div>
        </div>

        <ProgressBar value={result.score} showPercentage={false} />

        <div className="discipline-metrics">
          {coreMetrics.map(renderMetric)}
        </div>

        <div
          className="discipline-summary"
          aria-label="Today's behaviour summary"
        >
          <span>
            Stop violations: {disciplineSessionData.stopViolationCount}
          </span>
          <span>
            Impulse re-entries: {disciplineSessionData.impulseReentryCount}
          </span>
          <span>Early exits: {disciplineSessionData.earlyExitCount}</span>
          <span>Rule overrides: {disciplineSessionData.ruleOverrideCount}</span>
        </div>

        <div className="discipline-recommendation">
          <h4>Recommendation</h4>
          <p>{result.recommendation}</p>
        </div>

        <details className="discipline-details">
          <summary>Show {followUpMetrics.length} follow-up checks</summary>

          <div className="discipline-metrics discipline-follow-up">
            {followUpMetrics.map(renderMetric)}
          </div>
        </details>
      </div>
    </Panel>
  );
}
