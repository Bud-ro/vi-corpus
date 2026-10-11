import { Link } from "@tanstack/react-router";
import type { ComponentProps } from "react";

import { AppIcon } from "./AppIcon";

type BackButtonProps = {
  className?: string;
  label?: string;
  params?: Record<string, string>;
  search?: Record<string, unknown>;
  to: string;
};

export function BackButton({ className, label = "Back", params, search, to }: BackButtonProps) {
  const buttonClassName = ["back-button", className].filter(Boolean).join(" ");
  return (
    <Link
      aria-label={label}
      className={buttonClassName}
      params={params}
      search={search}
      title={label}
      to={to}
    >
      <AppIcon name="chevronLeft" size={18} />
    </Link>
  );
}

type BackIconButtonProps = Omit<ComponentProps<"button">, "children" | "className"> & {
  className?: string;
  label?: string;
};

export function BackIconButton({ className, label = "Back", ...props }: BackIconButtonProps) {
  const buttonClassName = ["back-button", className].filter(Boolean).join(" ");
  return (
    <button aria-label={label} className={buttonClassName} title={label} type="button" {...props}>
      <AppIcon name="chevronLeft" size={18} />
    </button>
  );
}
