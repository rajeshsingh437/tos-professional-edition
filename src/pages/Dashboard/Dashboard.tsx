import Panel from "../../components/common/Panel";
import StatCard from "../../components/common/StatCard";

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <div className="dashboard-grid">
        {/* KPI Cards */}

        <div className="kpi-grid">
          <StatCard
            title="Account Equity"
            value="₹10,00,000"
            subtitle="Total Trading Capital"
          />

          <StatCard
            title="Today's P/L"
            value="+₹8,450"
            subtitle="Open Profit"
            trend="positive"
          />

          <StatCard title="Win Rate" value="67.4%" subtitle="Last 100 Trades" />

          <StatCard
            title="Risk Used"
            value="0.65%"
            subtitle="Today's Risk"
            trend="negative"
          />
        </div>

        {/* Middle Section */}

        <div className="content-grid">
          <Panel title="Watchlist">
            <p>NIFTY</p>
            <p>BANKNIFTY</p>
            <p>RELIANCE</p>
            <p>HDFCBANK</p>
            <p>INFY</p>
          </Panel>

          <Panel title="Market Pulse">
            <p>India VIX</p>
            <p>USD / INR</p>
            <p>Brent Crude</p>
            <p>Gold</p>
            <p>Gift Nifty</p>
          </Panel>
        </div>

        {/* Bottom Section */}

        <div className="bottom-grid">
          <Panel title="Trading Notes">
            <p>• Wait for Opening Range</p>
            <p>• Avoid Overtrading</p>
            <p>• Respect Maximum Daily Loss</p>
          </Panel>

          <Panel title="Recent Trades">
            <p>No trades today.</p>
          </Panel>
        </div>
      </div>
    </div>
  );
}
