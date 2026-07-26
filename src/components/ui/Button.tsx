import "./button.css";

type ButtonVariant = "primary" | "secondary" | "success" | "danger";

interface ButtonProps {
  children: React.ReactNode;
  variant?: ButtonVariant;
  type?: "button" | "submit" | "reset";
  onClick?: () => void;
  disabled?: boolean;
}

export default function Button({
  children,
  variant = "primary",
  type = "button",
  onClick,
  disabled = false,
}: ButtonProps) {
  return (
    <button
      className={`tos-button ${variant}`}
      type={type}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
