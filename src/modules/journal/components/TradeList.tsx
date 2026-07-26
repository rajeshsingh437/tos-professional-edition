import "./TradeList.css";

export default function TradeList() {
  return (
    <div className="trade-list">
      <div className="trade-list-header">
        <div>
          <h2>Trade Explorer</h2>
          <p>Drafts • Active • Completed</p>
        </div>

        <button className="primary-button">+ New</button>
      </div>

      <input
        className="trade-search"
        type="search"
        placeholder="Search instrument or strategy..."
      />

      <div className="trade-group">
        <div className="trade-card active">
          <span className="status-badge draft">Draft</span>

          <div className="trade-card-title">NIFTY</div>

          <div className="trade-card-strategy">ORB Long</div>

          <div className="trade-card-footer">Today • 09:20</div>
        </div>

        <div className="trade-card">
          <span className="status-badge active-status">Active</span>

          <div className="trade-card-title">BANKNIFTY</div>

          <div className="trade-card-strategy">VWAP Reversal</div>

          <div className="trade-card-footer">Open Position</div>
        </div>

        <div className="trade-card">
          <span className="status-badge completed">Completed</span>

          <div className="trade-card-title">RELIANCE</div>

          <div className="trade-card-strategy">Breakout</div>

          <div className="trade-card-footer">Yesterday</div>
        </div>
      </div>
    </div>
  );
}
