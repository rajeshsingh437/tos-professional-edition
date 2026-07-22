import Panel from "../common/Panel";
import ProgressBar from "../common/ProgressBar";

import { sessionChecklist } from "../../constants/sessionChecklist";
import { calculateReadiness } from "../../utils/readinessEngine";

export default function SessionReadiness() {
  const result = calculateReadiness(sessionChecklist);

  const getStatusColor = () => {
    switch (result.status) {
      case "GO":
        return "#22c55e";
      case "CAUTION":
        return "#f59e0b";
      default:
        return "#ef4444";
    }
  };

  return (
    <Panel title="Session Readiness">
      <div className="session-readiness">
        <div className="readiness-status">
          <span className="status-text" style={{ color: getStatusColor() }}>
            {result.status}
          </span>

          <span className="readiness-score">{result.score}%</span>
        </div>

        <ProgressBar value={result.score} showPercentage={false} />

        <div className="checklist">
          {sessionChecklist.map((item) => (
            <div key={item.id} className="check-item">
              <span>{item.completed ? "✅" : "⬜"}</span>
              <span>{item.title}</span>
            </div>
          ))}
        </div>

        <div className="recommendation-box">
          <h4>Recommendation</h4>
          <p>{result.recommendation}</p>
        </div>
      </div>
    </Panel>
  );
}
