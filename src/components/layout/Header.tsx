import StatusBadge from "../common/StatusBadge";

export default function Header() {
  return (
    <header className="header">
      <div className="header-left">
        <h1>Trading Operating System</h1>

        <p>Professional Edition • Build 0.2.6 Alpha</p>
      </div>

      <div className="header-right">
        <StatusBadge text="Market Closed" type="danger" />

        <div className="user-profile">RS</div>
      </div>
    </header>
  );
}
