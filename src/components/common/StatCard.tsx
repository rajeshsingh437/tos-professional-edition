interface StatCardProps {
  title: string;
  value: string;
  subtitle: string;
  trend?: "positive" | "negative" | "neutral";
}

export default function StatCard({
  title,
  value,
  subtitle,
  trend = "neutral",
}: StatCardProps) {
  const trendClass =
    trend === "positive" ? "positive" : trend === "negative" ? "negative" : "";

  return (
    <div className="stat-card">
      <div className="stat-title">{title}</div>

      <div className={`stat-value ${trendClass}`}>{value}</div>

      <div className="stat-subtitle">{subtitle}</div>
    </div>
  );
}
