import { ShieldAlert, Target, TrendingUp, Wallet } from "lucide-react";

import MetricTile from "../common/MetricTile";

export default function DashboardCards() {
  const cards = [
    {
      label: "Account Equity",
      value: "₹10,00,000",
      subtitle: "Total Trading Capital",
      trend: "Protected",
      variant: "info" as const,
      icon: <Wallet size={26} />,
    },
    {
      label: "Today's P/L",
      value: "+₹8,450",
      subtitle: "Open Profit",
      trend: "+0.84%",
      variant: "success" as const,
      icon: <TrendingUp size={26} />,
    },
    {
      label: "Win Rate",
      value: "67.4%",
      subtitle: "Last 100 Trades",
      trend: "Above Target",
      variant: "success" as const,
      icon: <Target size={26} />,
    },
    {
      label: "Risk Used",
      value: "0.65%",
      subtitle: "Today's Risk",
      trend: "Safe",
      variant: "warning" as const,
      icon: <ShieldAlert size={26} />,
    },
  ];

  return (
    <div className="dashboard-cards">
      {cards.map((card) => (
        <MetricTile
          key={card.label}
          label={card.label}
          value={card.value}
          subtitle={card.subtitle}
          trend={card.trend}
          variant={card.variant}
          icon={card.icon}
        />
      ))}
    </div>
  );
}
