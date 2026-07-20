export default function OpenPositions() {
  const positions = [
    {
      symbol: "RELIANCE",
      side: "BUY",
      qty: 120,
      entry: "₹1,490",
      ltp: "₹1,496",
      pnl: "+₹720",
      positive: true,
    },
    {
      symbol: "NIFTY 25000 CE",
      side: "BUY",
      qty: 50,
      entry: "₹210",
      ltp: "₹228",
      pnl: "+₹900",
      positive: true,
    },
    {
      symbol: "BANKNIFTY FUT",
      side: "SELL",
      qty: 25,
      entry: "57,900",
      ltp: "57,980",
      pnl: "-₹2,000",
      positive: false,
    },
  ];

  return (
    <div className="positions-card">
      <h3>Open Positions</h3>

      {positions.map((trade) => (
        <div className="position-row" key={trade.symbol}>
          <div>
            <strong>{trade.symbol}</strong>
            <small>{trade.side}</small>
          </div>

          <div>
            <small>Qty</small>
            <strong>{trade.qty}</strong>
          </div>

          <div>
            <small>Entry</small>
            <strong>{trade.entry}</strong>
          </div>

          <div>
            <small>LTP</small>
            <strong>{trade.ltp}</strong>
          </div>

          <div>
            <small>P/L</small>

            <strong className={trade.positive ? "positive" : "negative"}>
              {trade.pnl}
            </strong>
          </div>
        </div>
      ))}
    </div>
  );
}
