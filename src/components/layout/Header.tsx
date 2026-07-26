import { Menu } from "lucide-react";

import { useSidebar } from "../../hooks/useSidebar";
import StatusBadge from "../common/StatusBadge";

export default function Header() {
  const { toggleSidebar } = useSidebar();

  return (
    <header className="header">
      <div className="header-left">
        <button
          type="button"
          className="sidebar-toggle"
          onClick={toggleSidebar}
          aria-label="Toggle sidebar"
        >
          <Menu size={22} />
        </button>

        <div>
          <h1>Trading Operating System</h1>
          <p>Professional Edition • Build 0.2.6 Alpha</p>
        </div>
      </div>

      <div className="header-right">
        <StatusBadge type="danger">Market Closed</StatusBadge>

        <div className="user-profile">RS</div>
      </div>
    </header>
  );
}
