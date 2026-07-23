import Panel from "../common/Panel";

const timeline = [
  { time: "08:45", task: "Session Readiness", status: "completed" },
  { time: "09:00", task: "Decision Engine", status: "completed" },
  { time: "09:30", task: "First Trade", status: "pending" },
  { time: "10:30", task: "Journal Update", status: "pending" },
  { time: "15:20", task: "End-of-Day Review", status: "pending" },
];

export default function TradingCommandCenter() {
  return (
    <Panel title="Trading Command Center">
      <div className="command-center">
        <section className="status-block">
          <h3>Today's Trading Status</h3>

          <div className="status-grid">
            <div>
              <span>Session</span>
              <strong className="positive">GO</strong>
            </div>

            <div>
              <span>Readiness</span>
              <strong>94%</strong>
            </div>

            <div>
              <span>Risk Used</span>
              <strong>0%</strong>
            </div>

            <div>
              <span>Max Risk</span>
              <strong>1%</strong>
            </div>

            <div>
              <span>Trades Left</span>
              <strong>3</strong>
            </div>

            <div>
              <span>Market</span>
              <strong>Closed</strong>
            </div>
          </div>
        </section>

        <section className="mission-block">
          <h3>Today's Mission</h3>

          <ul>
            <li>✅ Trade only A+ setups</li>
            <li>✅ Maximum 3 trades</li>
            <li>✅ Respect daily stop</li>
            <li>✅ Journal every trade</li>
            <li>✅ No averaging losers</li>
          </ul>
        </section>

        <section className="timeline-block">
          <h3>Today's Timeline</h3>

          {timeline.map((item) => (
            <div className="timeline-row" key={item.time}>
              <span>{item.time}</span>

              <span>{item.task}</span>

              <span>{item.status === "completed" ? "✔" : "○"}</span>
            </div>
          ))}
        </section>

        <section className="coach-block">
          <h3>AI Coach Preview</h3>

          <p>
            Discipline has improved over the last five sessions. Continue
            waiting for high-quality setups and avoid exiting winning trades too
            early.
          </p>
        </section>
      </div>
    </Panel>
  );
}
