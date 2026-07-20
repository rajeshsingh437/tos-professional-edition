export default function Header() {
  return (
    <header className="header">
      <div>
        <h2>Dashboard</h2>
        <p>Welcome to Trading Operating System</p>
      </div>

      <div className="header-right">
        <div className="market-status">
          <span className="market-dot"></span>
          Market Closed
        </div>

        <div className="user-profile">RS</div>
      </div>
    </header>
  );
}
