export default function Watchlist() {
  const stocks = [
    { symbol: "RELIANCE", price: "₹1,495.50", change: "+0.82%" },
    { symbol: "HDFCBANK", price: "₹1,972.20", change: "-0.45%" },
    { symbol: "INFY", price: "₹1,678.90", change: "+1.23%" },
    { symbol: "SBIN", price: "₹895.60", change: "+0.64%" },
    { symbol: "NIFTY 50", price: "25,482", change: "+0.64%" },
    { symbol: "BANKNIFTY", price: "57,810", change: "-0.21%" },
  ];

  return (
    <div className="watchlist-card">
      <h3>Watchlist</h3>

      {stocks.map((stock) => (
        <div className="watchlist-item" key={stock.symbol}>
          <div className="watch-symbol">{stock.symbol}</div>

          <div className="watch-price">{stock.price}</div>

          <div
            className={
              stock.change.startsWith("+") ? "watch-positive" : "watch-negative"
            }
          >
            {stock.change}
          </div>
        </div>
      ))}
    </div>
  );
}
