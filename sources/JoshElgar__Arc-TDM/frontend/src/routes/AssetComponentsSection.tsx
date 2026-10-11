import { Menu } from "@base-ui/react/menu";
import { Link, useNavigate } from "@tanstack/react-router";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";

import { api } from "../api/client";
import type {
  ComponentRecordingStartResponse,
  ComponentRecordingStopResponse,
  ComponentModelDefinition,
  ComponentSample,
  PlotlyFigure
} from "../api/types";
import { AppIcon } from "../components/AppIcon";
import { PlotlyChart } from "../components/PlotlyChart";
import { useWorkspaceId } from "./workspaceContext";

const markerLabels = ["drop event", "shake event", "temperature change"];

export function AssetComponentConsole({
  assetId,
  componentModel
}: {
  assetId: string;
  componentModel: ComponentModelDefinition;
}) {
  const workspaceId = useWorkspaceId();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const selected = componentModel;
  const [sampleRateHz, setSampleRateHz] = useState(componentModel.default_sample_rate_hz);
  const [sampleWindow, setSampleWindow] = useState(180);
  const [samples, setSamples] = useState<ComponentSample[]>([]);
  const [streamStatus, setStreamStatus] = useState<"connecting" | "live" | "offline">("connecting");
  const [recording, setRecording] = useState<ComponentRecordingStartResponse | null>(null);
  const [lastRecording, setLastRecording] = useState<ComponentRecordingStopResponse | null>(null);

  const latestSample = samples[samples.length - 1] ?? null;
  const plotFigure = useMemo(() => liveFigure(samples), [samples]);

  useEffect(() => {
    setSamples([]);
    setStreamStatus("connecting");
    const source = new EventSource(api.componentStreamUrl(workspaceId, assetId, sampleRateHz));
    source.onmessage = (event) => {
      const sample = JSON.parse(event.data) as ComponentSample;
      setSamples((current) => [...current.slice(-(sampleWindow - 1)), sample]);
      setStreamStatus("live");
    };
    source.onerror = () => {
      setStreamStatus("offline");
      source.close();
    };
    return () => source.close();
  }, [assetId, sampleRateHz, sampleWindow, workspaceId]);

  const startRecording = useMutation({
    mutationFn: () => {
      return api.startComponentRecording(workspaceId, assetId, sampleRateHz);
    },
    onSuccess: (nextRecording) => {
      setRecording(nextRecording);
      setLastRecording(null);
    }
  });
  const stopRecording = useMutation({
    mutationFn: () => {
      if (!recording) throw new Error("No recording is active.");
      return api.stopComponentRecording(workspaceId, assetId, recording.id);
    },
    onSuccess: (stopped) => {
      setRecording(null);
      setLastRecording(stopped);
      queryClient.invalidateQueries({ queryKey: ["assets", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["test-runs", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["files", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });
  const markEvent = useMutation({
    mutationFn: (label: string) => {
      if (!recording) throw new Error("Start recording first.");
      return api.markComponentRecording(workspaceId, assetId, recording.id, label);
    }
  });
  const createWorkbook = useMutation({
    mutationFn: () => {
      if (!lastRecording) throw new Error("No completed recording.");
      return api.createComponentWorkbook(workspaceId, assetId, lastRecording.id);
    },
    onSuccess: (workbook) => {
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbook", workspaceId, workbook.id] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
      navigate({ to: "/w/$workspaceId/workbooks/$workbookId", params: { workspaceId, workbookId: workbook.id } });
    }
  });

  return (
    <div className="components-page assets-page">
      <section className="assets-toolbar components-toolbar">
        <div className="component-top-toolbar">
          <div className="assets-title-group component-picker-group">
            <h2>{selected.name}</h2>
            <div className="component-doc-pill-row">
              {selected.docs.map((doc) => (
                <a href={doc.url} key={doc.url} rel="noreferrer" target="_blank">
                  <AppIcon name="link" />
                  <span>{doc.label}</span>
                </a>
              ))}
            </div>
            <div className="asset-chip-row component-tag-row">
              <span>{selected.kind}</span>
              <span>{selected.default_sample_rate_hz} Hz default</span>
              <span>{selected.channels.length} channels</span>
            </div>
          </div>
          <span className={`component-connection ${streamStatus}`}>
            <span />
            {streamStatus}
          </span>
        </div>

        <div className="component-recording-toolbar">
          <div className="component-recording-summary">
            {lastRecording ? (
              <>
                <strong>{lastRecording.sample_count} samples saved</strong>
                <Link params={{ workspaceId }} search={{ file: lastRecording.file_path }} to="/w/$workspaceId/data">
                  {lastRecording.file_path}
                </Link>
              </>
            ) : (
              <span>{recording ? recording.id : selected.vendor}</span>
            )}
          </div>
          <div className="component-recording-controls">
            <label className="component-number-input">
              <span>Sample rate</span>
              <input
                max={100}
                min={1}
                type="number"
                value={sampleRateHz}
                onChange={(event) => setSampleRateHz(Number(event.target.value))}
              />
            </label>
            <label className="component-number-input">
              <span>Window</span>
              <input
                max={1000}
                min={30}
                type="number"
                value={sampleWindow}
                onChange={(event) => {
                  const nextValue = Number(event.target.value);
                  setSampleWindow(Number.isFinite(nextValue) ? Math.max(1, nextValue) : 180);
                }}
              />
            </label>
            <AddEventMenu
              disabled={!recording || markEvent.isPending}
              onSelect={(label) => markEvent.mutate(label)}
            />
            {recording ? (
              <button
                className="button button-run"
                disabled={stopRecording.isPending}
                onClick={() => stopRecording.mutate()}
                type="button"
              >
                <AppIcon name={stopRecording.isPending ? "spinner" : "save"} />
                Stop recording
              </button>
            ) : (
              <button
                className="button button-primary"
                disabled={startRecording.isPending}
                onClick={() => startRecording.mutate()}
                type="button"
              >
                <AppIcon name={startRecording.isPending ? "spinner" : "play"} />
                Start recording
              </button>
            )}
            <button
              className="button"
              disabled={!lastRecording || createWorkbook.isPending}
              onClick={() => createWorkbook.mutate()}
              type="button"
            >
              <AppIcon name={createWorkbook.isPending ? "spinner" : "steps"} />
              Create workbook
            </button>
          </div>
        </div>
        {recordingError(startRecording.error, stopRecording.error, markEvent.error, createWorkbook.error)}
      </section>

      <section className="component-workspace">
        <section className="component-readings" aria-label="Live readings">
          <Reading label="Accel X" value={latestSample?.ax_g} unit="g" />
          <Reading label="Accel Y" value={latestSample?.ay_g} unit="g" />
          <Reading label="Accel Z" value={latestSample?.az_g} unit="g" />
          <Reading label="Temp" value={latestSample?.temperature_c} unit="C" />
        </section>

        <div className="panel component-live-panel">
          <PlotlyChart figure={plotFigure} />
        </div>
      </section>
    </div>
  );
}

function AddEventMenu({ disabled, onSelect }: { disabled: boolean; onSelect: (label: string) => void }) {
  return (
    <Menu.Root>
      <Menu.Trigger
        render={
          <button className="button component-event-trigger" disabled={disabled} type="button">
            <AppIcon name="plus" />
            Add Event
          </button>
        }
      />
      <Menu.Portal>
        <Menu.Positioner align="end" sideOffset={4}>
          <Menu.Popup className="file-tree-menu component-event-menu">
            {markerLabels.map((label) => (
              <Menu.Item className="file-tree-menu-item" key={label} onClick={() => onSelect(label)}>
                <span>{label}</span>
              </Menu.Item>
            ))}
          </Menu.Popup>
        </Menu.Positioner>
      </Menu.Portal>
    </Menu.Root>
  );
}

function Reading({ label, value, unit }: { label: string; value?: number; unit: string }) {
  return (
    <div className="asset-metric-tile component-reading">
      <span>{label}</span>
      <strong>{typeof value === "number" ? value.toFixed(unit === "C" ? 2 : 4) : "-"}</strong>
      <small>{unit}</small>
    </div>
  );
}

function liveFigure(samples: ComponentSample[]): PlotlyFigure {
  const x = samples.map((sample) => sample.sequence);
  const eventSamples = samples.filter((sample) => sample.event);
  return {
    data: [
      { x, y: samples.map((sample) => sample.ax_g), type: "scatter", mode: "lines", name: "Accel X" },
      { x, y: samples.map((sample) => sample.ay_g), type: "scatter", mode: "lines", name: "Accel Y" },
      { x, y: samples.map((sample) => sample.az_g), type: "scatter", mode: "lines", name: "Accel Z" },
      {
        x: eventSamples.map((sample) => sample.sequence),
        y: eventSamples.map((sample) => sample.az_g),
        text: eventSamples.map((sample) => sample.event),
        type: "scatter",
        mode: "markers+text",
        name: "Events",
        textposition: "top center"
      }
    ],
    layout: {
      height: 360,
      margin: { l: 42, r: 18, t: 16, b: 38 },
      xaxis: { title: "Sample" },
      yaxis: { title: "g" },
      showlegend: true
    }
  };
}

function recordingError(...errors: unknown[]) {
  const error = errors.find((candidate) => candidate instanceof Error) as Error | undefined;
  return error ? <p className="inline-error">{error.message}</p> : null;
}
