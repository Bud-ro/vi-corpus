type HtmlPreviewProps = {
  className?: string;
  title: string;
  url: string;
};

export function HtmlPreview({ className = "html-preview-frame", title, url }: HtmlPreviewProps) {
  return <iframe className={className} src={url} title={title} sandbox="" />;
}
