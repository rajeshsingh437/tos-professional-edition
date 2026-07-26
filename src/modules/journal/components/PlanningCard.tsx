import "./PlanningCard.css";

export default function PlanningCard() {
  return (
    <section className="planning-card">
      <div className="planning-header">
        <h2>Planning</h2>
        <span>Trade Setup</span>
      </div>

      <div className="planning-grid">
        <div className="planning-field">
          <label>Instrument</label>
          <div className="field-value">NIFTY</div>
        </div>

        <div className="planning-field">
          <label>Direction</label>
          <div className="field-value">Long</div>
        </div>

        <div className="planning-field">
          <label>Strategy</label>
          <div className="field-value">ORB Long</div>
        </div>

        <div className="planning-field">
          <label>Timeframe</label>
          <div className="field-value">Intraday</div>
        </div>

        <div className="planning-field">
          <label>Entry Price</label>
          <div className="field-value">—</div>
        </div>

        <div className="planning-field">
          <label>Stop Loss</label>
          <div className="field-value">—</div>
        </div>

        <div className="planning-field">
          <label>Target</label>
          <div className="field-value">—</div>
        </div>

        <div className="planning-field">
          <label>Position Size</label>
          <div className="field-value">—</div>
        </div>

        <div className="planning-field planning-wide">
          <label>Trade Thesis</label>

          <div className="notes-box">
            Describe why this trade has an edge...
          </div>
        </div>
      </div>
    </section>
  );
}
