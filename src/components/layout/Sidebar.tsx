import {
  BarChart3,
  Bot,
  ClipboardList,
  LayoutDashboard,
  LineChart,
  Settings,
  ShieldCheck,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const menuItems = [
  {
    name: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Trading",
    path: "/trading",
    icon: LineChart,
  },
  {
    name: "Journal",
    path: "/journal",
    icon: ClipboardList,
  },
  {
    name: "Analytics",
    path: "/analytics",
    icon: BarChart3,
  },
  {
    name: "Risk Manager",
    path: "/risk",
    icon: ShieldCheck,
  },
  {
    name: "AI Assistant",
    path: "/ai",
    icon: Bot,
  },
  {
    name: "Settings",
    path: "/settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">
        <h1>TOS</h1>
        <span>Professional Edition</span>
      </div>

      <nav className="sidebar-menu">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.name}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `menu-item ${isActive ? "active" : ""}`
              }
            >
              <Icon className="menu-icon" size={20} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="version">TOS Professional Edition</div>
        <div className="build">v0.2.0-alpha.2</div>
        <div className="status">
          <span className="status-dot"></span>
          Development Build
        </div>
      </div>
    </aside>
  );
}
