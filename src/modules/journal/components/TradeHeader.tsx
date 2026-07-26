import "./TradeHeader.css";

export default function TradeHeader() {
  return (
    <section className="trade-header">
      <div className="trade-header-top">
        <div>
          <h1>NIFTY</h1>
          <span className="trade-status draft">Draft</span>
        </div>

        <div className="trade-actions">
          <button className="secondary-button">Validate</button>

          <button className="primary-button">Save Trade</button>
        </div>
      </div>

      <div className="trade-meta-grid">
        <div>
          <span>Strategy</span>
          <strong>ORB Long</strong>
        </div>

        <div>
          <span>Direction</span>
          <strong>Long</strong>
        </div>

        <div>
          <span>Timeframe</span>
          <strong>Intraday</strong>
        </div>

        <div>
          <span>Trade ID</span>
          <strong>TRD-001</strong>
        </div>

        <div>
          <span>Risk</span>
          <strong>₹2,500</strong>
        </div>

        <div>
          <span>Reward / Risk</span>
          <strong>1 : 2</strong>
        </div>
      </div>
    </section>
  );
}
