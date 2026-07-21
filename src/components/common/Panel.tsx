import type { ReactNode } from "react";

interface PanelProps {
  title: string;
  children: ReactNode;
  action?: ReactNode;
}

export default function Panel({ title, children, action }: PanelProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h3>{title}</h3>

        {action && <div className="panel-action">{action}</div>}
      </div>

      <div className="panel-body">{children}</div>
    </section>
  );
}
