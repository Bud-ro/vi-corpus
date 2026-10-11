import type { CSSProperties } from "react";
import { useEffect, useRef } from "react";

import type { PlotlyFigure } from "../api/types";

type PlotlyApi = {
  react: (
    element: HTMLDivElement,
    data: unknown[],
    layout: Record<string, unknown>,
    config?: Record<string, unknown>
  ) => Promise<void>;
  purge: (element: HTMLDivElement) => void;
  relayout: (element: HTMLDivElement, update: Record<string, unknown>) => Promise<void>;
};

export function PlotlyChart({ figure }: { figure: PlotlyFigure }) {
  const ref = useRef<HTMLDivElement | null>(null);
  const plotlyRef = useRef<PlotlyApi | null>(null);
  const renderTokenRef = useRef(0);
  const height = figureHeight(figure.layout);
  const plotStyle: CSSProperties | undefined = height ? { height } : undefined;

  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const plotElement = element;

    const renderToken = renderTokenRef.current + 1;
    renderTokenRef.current = renderToken;
    let cancelled = false;

    async function render() {
      const Plotly = (await import("plotly.js-basic-dist-min")) as unknown as PlotlyApi;
      if (cancelled || renderTokenRef.current !== renderToken) return;
      plotlyRef.current = Plotly;
      const styles = getComputedStyle(document.documentElement);
      const textColor = styles.getPropertyValue("--color-text").trim();
      const borderColor = styles.getPropertyValue("--color-border").trim();
      const palette = [
        styles.getPropertyValue("--color-chart-1").trim(),
        styles.getPropertyValue("--color-chart-2").trim(),
        styles.getPropertyValue("--color-chart-3").trim()
      ];
      await Plotly.react(
        plotElement,
        applyTracePalette(figure.data ?? [], palette),
        {
          paper_bgcolor: "transparent",
          plot_bgcolor: "transparent",
          colorway: palette,
          font: { color: textColor },
          xaxis: { gridcolor: borderColor, zerolinecolor: borderColor },
          yaxis: { gridcolor: borderColor, zerolinecolor: borderColor },
          ...responsiveLayout(figure.layout, height),
          autosize: true
        },
        { displayModeBar: false, doubleClick: "reset", responsive: true }
      );
    }
    render();
    return () => {
      cancelled = true;
      import("plotly.js-basic-dist-min").then((Plotly) => {
        if (renderTokenRef.current === renderToken) {
          (Plotly as unknown as PlotlyApi).purge(plotElement);
          plotlyRef.current = null;
        }
      });
    };
  }, [figure]);

  function handleDoubleClick() {
    const element = ref.current;
    const Plotly = plotlyRef.current;
    if (!element || !Plotly) return;
    Plotly.relayout(element, resetAxisRanges(figure.layout)).catch(() => {
      // Plotly may already be tearing down during navigation.
    });
  }

  return <div className="plot" ref={ref} style={plotStyle} onDoubleClick={handleDoubleClick} />;
}

function responsiveLayout(layout: Record<string, unknown> | undefined, height: number | undefined) {
  const normalized = { ...(layout ?? {}) };
  delete normalized.width;
  delete normalized.height;
  if (height) {
    normalized.height = height;
  }
  return normalized;
}

function figureHeight(layout: Record<string, unknown> | undefined) {
  const height = layout?.height;
  if (typeof height !== "number" || !Number.isFinite(height) || height <= 0) {
    return undefined;
  }
  return Math.max(240, height);
}

function applyTracePalette(data: unknown[], palette: string[]) {
  return data.map((trace, index) => {
    const normalizedTrace = normalizePlotlyValue(trace);
    if (!isRecord(normalizedTrace)) return normalizedTrace;
    const color = palette[index % palette.length];
    return {
      ...normalizedTrace,
      marker: normalizedTrace.marker ?? { color },
      line: normalizedTrace.line ?? { color }
    };
  });
}

function resetAxisRanges(layout: Record<string, unknown> | undefined) {
  const axisKeys = new Set(["xaxis", "yaxis"]);
  for (const key of Object.keys(layout ?? {})) {
    if (/^[xy]axis\d*$/.test(key)) {
      axisKeys.add(key);
    }
  }

  const update: Record<string, unknown> = {};
  for (const axisKey of axisKeys) {
    const axis = layout?.[axisKey];
    if (isRecord(axis) && Array.isArray(axis.range)) {
      update[`${axisKey}.range`] = axis.range;
      update[`${axisKey}.autorange`] = false;
    } else {
      update[`${axisKey}.autorange`] = true;
    }
  }
  return update;
}

function normalizePlotlyValue(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(normalizePlotlyValue);
  }
  if (!isRecord(value)) {
    return value;
  }

  const decoded = decodeTypedArray(value);
  if (decoded) {
    return decoded;
  }

  const normalized: Record<string, unknown> = {};
  for (const [key, nestedValue] of Object.entries(value)) {
    normalized[key] = normalizePlotlyValue(nestedValue);
  }
  return normalized;
}

function decodeTypedArray(value: Record<string, unknown>) {
  if (typeof value.dtype !== "string" || typeof value.bdata !== "string") {
    return null;
  }

  const reader = typedArrayReader(value.dtype);
  if (!reader) return null;

  const binary = atob(value.bdata);
  const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0));
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const values: number[] = [];
  for (let offset = 0; offset + reader.byteLength <= view.byteLength; offset += reader.byteLength) {
    values.push(reader.read(view, offset));
  }
  return values;
}

function typedArrayReader(dtype: string) {
  const cleanType = dtype.replace(/[<>=|]/g, "");
  const littleEndian = !dtype.startsWith(">");
  switch (cleanType) {
    case "f8":
      return {
        byteLength: 8,
        read: (view: DataView, offset: number) => view.getFloat64(offset, littleEndian)
      };
    case "f4":
      return {
        byteLength: 4,
        read: (view: DataView, offset: number) => view.getFloat32(offset, littleEndian)
      };
    case "i1":
      return {
        byteLength: 1,
        read: (view: DataView, offset: number) => view.getInt8(offset)
      };
    case "i2":
      return {
        byteLength: 2,
        read: (view: DataView, offset: number) => view.getInt16(offset, littleEndian)
      };
    case "i4":
      return {
        byteLength: 4,
        read: (view: DataView, offset: number) => view.getInt32(offset, littleEndian)
      };
    case "u1":
      return {
        byteLength: 1,
        read: (view: DataView, offset: number) => view.getUint8(offset)
      };
    case "u2":
      return {
        byteLength: 2,
        read: (view: DataView, offset: number) => view.getUint16(offset, littleEndian)
      };
    case "u4":
      return {
        byteLength: 4,
        read: (view: DataView, offset: number) => view.getUint32(offset, littleEndian)
      };
    default:
      return null;
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}
