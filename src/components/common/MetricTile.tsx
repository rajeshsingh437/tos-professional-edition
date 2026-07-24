import type { ReactNode } from "react";

type MetricVariant = "default" | "success" | "warning" | "danger" | "info";

interface MetricTileProps {
  label: string;
  value: ReactNode;
  subtitle?: string;
  trend?: ReactNode;
  icon?: ReactNode;
  variant?: MetricVariant;
}

export default function MetricTile({
  label,
  value,
  subtitle,
  trend,
  icon,
  variant = "default",
}: MetricTileProps) {
  return (
    <div className={`metric-tile metric-${variant}`}>
      <div className="metric-top">
        <div>
          <div className="metric-label">{label}</div>

          <div className="metric-value">{value}</div>
        </div>

        {icon && <div className="metric-icon">{icon}</div>}
      </div>

      {(subtitle || trend) && (
        <div className="metric-footer">
          {subtitle && <span className="metric-subtitle">{subtitle}</span>}

          {trend && <span className="metric-trend">{trend}</span>}
        </div>
      )}
    </div>
  );
}
