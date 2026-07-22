interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  action?: string;
}

export default function SectionHeader({
  title,
  subtitle,
  action,
}: SectionHeaderProps) {
  return (
    <div className="section-header">
      <div>
        <h2>{title}</h2>

        {subtitle && <p>{subtitle}</p>}
      </div>

      {action && <span className="section-action">{action}</span>}
    </div>
  );
}
