import "./TradeBookPage.css";

export default function TradeBookPage() {
  return (
    <div className="trade-book-page">
      <section className="journal-hero">
        <div>
          <span className="journal-tag">TRADE LIFECYCLE ENGINE</span>

          <h1>Trading Journal</h1>

          <p>
            Every trade begins with a plan, follows a disciplined execution, and
            ends with a structured review.
          </p>
        </div>

        <button className="plan-trade-button">+ Plan New Trade</button>
      </section>

      <section className="journal-summary">
        <div className="summary-card">
          <h3>Today's Progress</h3>

          <div className="summary-item">
            Planned Trades
            <strong>0</strong>
          </div>

          <div className="summary-item">
            Active Trades
            <strong>0</strong>
          </div>

          <div className="summary-item">
            Completed Trades
            <strong>0</strong>
          </div>

          <div className="summary-item">
            Awaiting Review
            <strong>0</strong>
          </div>
        </div>

        <div className="trade-book-panel">
          <div className="panel-header">
            <h2>Trade Book</h2>
          </div>

          <div className="empty-state">
            <div className="empty-icon">📒</div>

            <h3>No Trades Yet</h3>

            <p>
              Your trading history will appear here once your first trade has
              been planned and executed.
            </p>

            <button className="primary-button">Plan First Trade</button>
          </div>
        </div>
      </section>
    </div>
  );
}
