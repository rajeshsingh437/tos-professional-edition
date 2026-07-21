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
  return (
    <div className={`stat-card ${trend}`}>
      <div className="stat-title">{title}</div>

      <div className="stat-value">{value}</div>

      <div className="stat-subtitle">{subtitle}</div>
    </div>
  );
}
