import MarketRow from "../../components/common/MarketRow";
import Panel from "../../components/common/Panel";
import SectionHeader from "../../components/common/SectionHeader";
import StatCard from "../../components/common/StatCard";
import SessionReadiness from "../../components/dashboard/SessionReadiness";

import { dashboardStats } from "../../constants/dashboardData";
import { marketPulse } from "../../constants/dashboardLists";

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <SectionHeader
        title="Trading Dashboard"
        subtitle="Professional Trading Workspace"
        action="LIVE"
      />

      {/* ======================================================
          SESSION READINESS
      ======================================================= */}

      <div style={{ marginBottom: "24px" }}>
        <SessionReadiness />
      </div>

      {/* ======================================================
          KPI CARDS
      ======================================================= */}

      <div className="dashboard-grid">
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

          <Panel title="Recent Trades">
            <p>No trades today.</p>
          </Panel>

          <Panel title="Today's Mission">
            <ul>
              <li>✅ Protect Capital</li>
              <li>✅ Follow Trading Plan</li>
              <li>✅ Respect Stop Loss</li>
              <li>✅ No Impulsive Re-entry</li>
            </ul>
          </Panel>
        </div>
      </div>
    </div>
  );
}
