import type React from "react";

type PageHeaderProps = {
  title: string;
  eyebrow?: string;
  actions?: React.ReactNode;
};

export function PageHeader({ title, eyebrow, actions }: PageHeaderProps) {
  return (
    <header className="page-header">
      <div>
        {eyebrow && <div className="eyebrow">{eyebrow}</div>}
        <h1>{title}</h1>
      </div>
      {actions && <div className="header-actions">{actions}</div>}
    </header>
  );
}
