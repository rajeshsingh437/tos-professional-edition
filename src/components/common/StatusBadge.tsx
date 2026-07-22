interface StatusBadgeProps {
  text: string;
  type?: "success" | "danger" | "warning" | "info";
}

export default function StatusBadge({ text, type = "info" }: StatusBadgeProps) {
  return (
    <div className={`status-badge ${type}`}>
      <span className="status-dot"></span>

      {text}
    </div>
  );
}
