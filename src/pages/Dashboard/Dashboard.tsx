import MarketRow from "../../components/common/MarketRow";
import Panel from "../../components/common/Panel";
import StatCard from "../../components/common/StatCard";

import { dashboardStats } from "../../constants/dashboardData";
import {
  marketPulse,
  tradingNotes,
  watchlist,
} from "../../constants/dashboardLists";

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <div className="dashboard-grid">
        {/* ===========================
            KPI CARDS
        =========================== */}

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

        {/* ===========================
            MAIN CONTENT
        =========================== */}

        <div className="content-grid">
          {/* WATCHLIST */}

          <Panel title="Watchlist">
            <MarketRow
              symbol={watchlist[0]}
              value="25,250"
              change="+0.65%"
              positive
            />

            <MarketRow
              symbol={watchlist[1]}
              value="57,890"
              change="-0.42%"
              positive={false}
            />

            <MarketRow
              symbol={watchlist[2]}
              value="1,622"
              change="+1.18%"
              positive
            />

            <MarketRow
              symbol={watchlist[3]}
              value="2,070"
              change="+0.31%"
              positive
            />

            <MarketRow
              symbol={watchlist[4]}
              value="1,715"
              change="-0.15%"
              positive={false}
            />
          </Panel>

          {/* MARKET PULSE */}

          <Panel title="Market Pulse">
            <ul>
              {marketPulse.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </Panel>

          {/* TRADING NOTES */}

          <Panel title="Trading Notes">
            <ul>
              {tradingNotes.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          </Panel>

          {/* RECENT TRADES */}

          <Panel title="Recent Trades">
            <p>No trades today.</p>
          </Panel>
        </div>
      </div>
    </div>
  );
}
