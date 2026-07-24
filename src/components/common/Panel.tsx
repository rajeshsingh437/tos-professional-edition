import type { ReactNode } from "react";

interface PanelProps {
  title: string;
  children: ReactNode;

  subtitle?: string;
  status?: ReactNode;
  action?: ReactNode;
  footer?: ReactNode;

  accent?: "default" | "success" | "warning" | "danger" | "info" | "purple";

  className?: string;
}

export default function Panel({
  title,
  subtitle,
  status,
  action,
  footer,
  accent = "default",
  className = "",
  children,
}: PanelProps) {
  return (
    <section className={`panel panel-${accent} ${className}`.trim()}>
      <div className="panel-header">
        <div className="panel-heading">
          <div className="panel-title-row">
            <h3 className="panel-title">{title}</h3>

            {status && <div className="panel-status">{status}</div>}
          </div>

          {subtitle && <p className="panel-subtitle">{subtitle}</p>}
        </div>

        {action && <div className="panel-action">{action}</div>}
      </div>

      <div className="panel-body">{children}</div>

      {footer && <div className="panel-footer">{footer}</div>}
    </section>
  );
}
