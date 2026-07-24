import type { ReactNode } from "react";

type StatusType =
  | "success"
  | "warning"
  | "danger"
  | "info"
  | "neutral"
  | "purple";

interface StatusBadgeProps {
  type?: StatusType;
  children: ReactNode;
}

export default function StatusBadge({
  type = "neutral",
  children,
}: StatusBadgeProps) {
  return <span className={`status-badge status-${type}`}>{children}</span>;
}
