type PageLoadingProps = {
  className?: string;
  label?: string;
};

export function PageLoading({ className, label = "Loading" }: PageLoadingProps) {
  return (
    <div
      aria-label={label}
      aria-live="polite"
      className={["page", "page-loading", className].filter(Boolean).join(" ")}
      role="status"
    >
      <div className="page-loading-inner">
        <span aria-hidden="true" className="thinking-dots">
          <span />
          <span />
          <span />
        </span>
      </div>
    </div>
  );
}
