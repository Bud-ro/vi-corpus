from __future__ import annotations

REPORT_HTML_CONTRACT = """
Report HTML style contract:
- Every report HTML file must be a complete, self-contained document.
- Use this shell: <body class="arc-report-canvas"><article class="arc-report-page">...</article></body>.
- Put the title, summary, and metadata inside <header class="arc-report-header">.
- Use <section class="arc-report-section"> for narrative sections.
- Use <figure class="arc-report-figure"> for charts, tables, images, and important evidence.
- Keep the look like a sparse technical document: white page, gray outer canvas, generous margins,
  strong type hierarchy, thin borders, compact tables, no gradients, no decorative cards.
- Include the CSS below inline in <style>. You may add tiny report-specific CSS, but keep these
  class names and the overall document style.

Required baseline CSS:
body.arc-report-canvas {
  margin: 0;
  background: #f4f4f3;
  color: #242424;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.55;
}
.arc-report-page {
  width: min(920px, calc(100vw - 64px));
  margin: 56px auto;
  background: #fff;
  border: 1px solid #dededb;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  padding: 56px 56px 64px;
}
.arc-report-header {
  margin-bottom: 44px;
}
.arc-report-kicker {
  color: #777;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}
.arc-report-icon {
  display: inline-grid;
  place-items: center;
  width: 48px;
  height: 48px;
  margin-bottom: 28px;
  background: #f1f1f0;
  color: #6f6f6c;
  border: 1px solid #e3e3e0;
  font-size: 24px;
}
.arc-report-page h1 {
  margin: 0 0 12px;
  font-size: 38px;
  line-height: 1.12;
  font-weight: 620;
}
.arc-report-summary {
  max-width: 760px;
  margin: 0 0 18px;
  color: #6c6c68;
  font-size: 17px;
}
.arc-report-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  margin-top: 22px;
  color: #73736f;
  font-size: 14px;
}
.arc-report-section {
  margin-top: 38px;
}
.arc-report-section h2 {
  margin: 0 0 12px;
  font-size: 25px;
  line-height: 1.2;
  font-weight: 610;
}
.arc-report-section p,
.arc-report-section li {
  color: #696966;
  font-size: 16px;
}
.arc-report-section ul {
  padding-left: 22px;
}
.arc-report-figure {
  margin: 28px 0 0;
  border: 1px solid #dfdfdc;
  background: #fff;
}
.arc-report-figure figcaption {
  padding: 10px 14px;
  border-bottom: 1px solid #e8e8e5;
  color: #333;
  font-size: 14px;
  font-weight: 650;
}
.arc-report-figure-body {
  padding: 14px;
}
.arc-report-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
.arc-report-table th,
.arc-report-table td {
  padding: 9px 10px;
  border-bottom: 1px solid #ececea;
  text-align: left;
  vertical-align: top;
}
.arc-report-table th {
  color: #555;
  font-weight: 650;
  background: #fafaf9;
}
.arc-report-note {
  margin-top: 24px;
  padding-top: 14px;
  border-top: 1px solid #e5e5e2;
  color: #777;
  font-size: 13px;
}
@media (max-width: 720px) {
  .arc-report-page {
    width: auto;
    margin: 0;
    border-width: 0;
    padding: 32px 22px 44px;
  }
  .arc-report-page h1 {
    font-size: 30px;
  }
}
""".strip()
