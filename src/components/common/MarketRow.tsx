interface MarketRowProps {
  symbol: string;
  value?: string;
  change?: string;
  positive?: boolean;
}

export default function MarketRow({
  symbol,
  value,
  change,
  positive = true,
}: MarketRowProps) {
  return (
    <div className="market-row">
      <div className="market-symbol">{symbol}</div>

      <div className="market-values">
        {value && <span className="market-price">{value}</span>}

        {change && (
          <span
            className={
              positive ? "market-change positive" : "market-change negative"
            }
          >
            {change}
          </span>
        )}
      </div>
    </div>
  );
}
