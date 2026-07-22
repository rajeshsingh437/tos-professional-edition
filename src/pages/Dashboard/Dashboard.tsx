import MarketRow from "../../components/common/MarketRow";
import Panel from "../../components/common/Panel";
import SectionHeader from "../../components/common/SectionHeader";
import StatCard from "../../components/common/StatCard";

import { dashboardStats } from "../../constants/dashboardData";
import { marketPulse, tradingNotes } from "../../constants/dashboardLists";

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <SectionHeader
        title="Trading Dashboard"
        subtitle="Professional Trading Workspace"
        action="LIVE"
      />

      <div className="dashboard-grid">
        {/* ======================================================
            KPI CARDS
        ======================================================= */}

        <div className="kpi-grid">
          {dashboardStats.map((stat) => (
            <StatCard
              key={stat.title}
              title={stat.title}
              value={stat.value}
              subtitle={stat.subtitle}
              trend={stat.trend}
            />
          ))}
        </div>

        {/* ======================================================
            MAIN CONTENT
        ======================================================= */}

        <div className="content-grid">
          <Panel title="Watchlist">
            <MarketRow symbol="NIFTY" value="25,250" change="+0.65%" positive />

            <MarketRow
              symbol="BANKNIFTY"
              value="57,890"
              change="-0.42%"
              positive={false}
            />

            <MarketRow
              symbol="RELIANCE"
              value="1,622"
              change="+1.18%"
              positive
            />

            <MarketRow
              symbol="HDFCBANK"
              value="2,070"
              change="+0.31%"
              positive
            />

            <MarketRow
              symbol="INFY"
              value="1,715"
              change="-0.15%"
              positive={false}
            />
          </Panel>

          <Panel title="Market Pulse">
            <ul>
              {marketPulse.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </Panel>

          <Panel title="Trading Notes">
            <ul>
              {tradingNotes.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </Panel>

          <Panel title="Recent Trades">
            <p>No trades today.</p>
          </Panel>
        </div>
      </div>
    </div>
  );
}
