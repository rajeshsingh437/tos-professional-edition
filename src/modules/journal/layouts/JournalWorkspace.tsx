import PlanningCard from "../components/PlanningCard";
import TradeHeader from "../components/TradeHeader";
import TradeExplorer from "../components/TradeList";

import "../styles/JournalWorkspace.css";

export default function JournalWorkspace() {
  return (
    <div className="journal-workspace">
      <aside className="workspace-sidebar">
        <TradeExplorer />
      </aside>

      <section className="workspace-main">
        <TradeHeader />

        <nav className="tle-tabs">
          <button className="tle-tab active">Planning</button>

          <button className="tle-tab">Readiness</button>

          <button className="tle-tab">Validation</button>

          <button className="tle-tab">Execution</button>

          <button className="tle-tab">Review</button>

          <button className="tle-tab">Learning</button>
        </nav>

        <PlanningCard />
      </section>
    </div>
  );
}
