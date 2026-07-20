import "./App.css";

import Header from "./components/layout/Header";
import MainLayout from "./components/layout/MainLayout";
import Sidebar from "./components/layout/Sidebar";

import DashboardCards from "./components/dashboard/DashboardCards";
import EquityCurve from "./components/dashboard/EquityCurve";
import MarketPulse from "./components/dashboard/MarketPulse";
import OpenPositions from "./components/dashboard/OpenPositions";
import RecentTrades from "./components/dashboard/RecentTrades";
import Watchlist from "./components/dashboard/Watchlist";

function App() {
  return (
    <MainLayout>
      <Sidebar />

      <main className="content">
        <Header />

        <DashboardCards />

        <div className="dashboard-row">
          <MarketPulse />
          <Watchlist />
        </div>

        <EquityCurve />

        <div className="dashboard-row">
          <RecentTrades />
          <OpenPositions />
        </div>
      </main>
    </MainLayout>
  );
}

export default App;
