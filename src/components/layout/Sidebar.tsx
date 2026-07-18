import {
  LayoutDashboard,
  BriefcaseBusiness,
  ClipboardList,
  BarChart3,
  ShieldCheck,
  Settings,
} from "lucide-react";

const menuItems = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Portfolio",
    icon: BriefcaseBusiness,
  },
  {
    name: "Trading Journal",
    icon: ClipboardList,
  },
  {
    name: "Analytics",
    icon: BarChart3,
  },
  {
    name: "Risk Manager",
    icon: ShieldCheck,
  },
  {
    name: "Settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">
        <h2>TOS</h2>
        <span>Professional Edition</span>
      </div>

      <nav>
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.name}
              className="menu-item"
            >
              <Icon size={20} />

              <span>{item.name}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        Build 0.1.002-B
      </div>
    </aside>
  );
}