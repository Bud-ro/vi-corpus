export function ArcLogo({ className }: { className?: string }) {
  return <span className={["arc-logo", className].filter(Boolean).join(" ")}>ARC</span>;
}
