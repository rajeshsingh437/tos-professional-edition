export default function MarketPulse() {
  return (
    <div className="market-pulse-card">
      <div className="pulse-header">
        <h3>Market Pulse</h3>
        <span className="market-status">LIVE</span>
      </div>

      <div className="pulse-grid">
        <div>
          <small>NIFTY</small>
          <h2>25,482</h2>
          <span className="positive">+0.64%</span>
        </div>

        <div>
          <small>BANKNIFTY</small>
          <h2>57,810</h2>
          <span className="negative">-0.21%</span>
        </div>

        <div>
          <small>India VIX</small>
          <h2>13.8</h2>
          <span>Low Volatility</span>
        </div>
      </div>
    </div>
  );
}
