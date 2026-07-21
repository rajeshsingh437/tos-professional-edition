export default function Header() {
  const today = new Date().toLocaleDateString("en-IN", {
    weekday: "long",
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  return (
    <header className="header">
      <div className="header-left">
        <h1>Dashboard</h1>
        <p>Welcome back, Rajesh 👋</p>
      </div>

      <div className="header-right">
        <div className="header-date">
          <span className="label">Today</span>
          <strong>{today}</strong>
        </div>

        <div className="market-status">
          <span className="market-dot"></span>
          Market Closed
        </div>

        <div className="user-profile">
          <span>RS</span>
        </div>
      </div>
    </header>
  );
}
