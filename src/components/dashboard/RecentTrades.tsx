export default function RecentTrades() {
  const trades = [
    {
      time: "09:18",
      symbol: "NIFTY",
      type: "BUY",
      pnl: "+₹2,450",
    },
    {
      time: "10:02",
      symbol: "BANKNIFTY",
      type: "SELL",
      pnl: "-₹850",
    },
    {
      time: "11:27",
      symbol: "RELIANCE",
      type: "BUY",
      pnl: "+₹1,120",
    },
    {
      time: "12:45",
      symbol: "INFY",
      type: "EXIT",
      pnl: "+₹630",
    },
  ];

  return (
    <div className="recent-trades-card">
      <h3>Recent Trades</h3>

      {trades.map((trade) => (
        <div className="trade-row" key={trade.time + trade.symbol}>
          <div>
            <strong>{trade.symbol}</strong>
            <small>{trade.time}</small>
          </div>

          <span>{trade.type}</span>

          <span className={trade.pnl.startsWith("+") ? "positive" : "negative"}>
            {trade.pnl}
          </span>
        </div>
      ))}
    </div>
  );
}
