import {
  LayoutDashboard,
  BriefcaseBusiness,
  ClipboardList,
  ShieldCheck,
  BarChart3,
  Settings,
} from "lucide-react";

const menu = [
  { icon: LayoutDashboard, label: "Dashboard" },
  { icon: BriefcaseBusiness, label: "Portfolio" },
  { icon: ClipboardList, label: "Trade Desk" },
  { icon: ShieldCheck, label: "Risk Command" },
  { icon: BarChart3, label: "Analytics" },
  { icon: Settings, label: "Settings" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <h2 className="logo">TOS</h2>

      <nav>
        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className="nav-item"
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}