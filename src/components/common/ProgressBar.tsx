interface ProgressBarProps {
  value: number;
  max?: number;
  label?: string;
  showPercentage?: boolean;
}

export default function ProgressBar({
  value,
  max = 100,
  label,
  showPercentage = true,
}: ProgressBarProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  const getStatusClass = () => {
    if (percentage >= 90) return "progress-success";
    if (percentage >= 70) return "progress-warning";
    return "progress-danger";
  };

  return (
    <div className="progress-wrapper">
      {(label || showPercentage) && (
        <div className="progress-header">
          {label && <span className="progress-label">{label}</span>}

          {showPercentage && (
            <span className="progress-value">{Math.round(percentage)}%</span>
          )}
        </div>
      )}

      <div className="progress-track">
        <div
          className={`progress-fill ${getStatusClass()}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
