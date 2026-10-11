import type { FormEvent } from "react";

import { AppIcon } from "../components/AppIcon";
import { AppSelect } from "../components/AppSelect";

export type RunDraft = {
  id: string;
  name: string;
  assetId: string;
  startTime: string;
  endTime: string;
  notes: string;
};

export function RunForm({
  assets,
  draft,
  error,
  pending,
  onCancel,
  onChange,
  onSubmit
}: {
  assets: Array<{ id: string; name: string }>;
  draft: RunDraft;
  error?: string | null;
  pending: boolean;
  onCancel: () => void;
  onChange: (patch: Partial<RunDraft>) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <form className="asset-form run-form" onSubmit={onSubmit}>
      <div className="asset-form-header">
        <div>
          <h2>{draft.id ? "Edit run" : "New run"}</h2>
          <p>A run is a real test session for one asset. Attach data in workbooks.</p>
        </div>
      </div>
      <div className="asset-form-grid">
        <label className="settings-field">
          <span>Title</span>
          <input value={draft.name} onChange={(event) => onChange({ name: event.target.value })} />
        </label>
        <div className="settings-field">
          <span>Asset</span>
          <AppSelect
            ariaLabel="Select run asset"
            options={assets.map((asset) => ({ label: asset.name, value: asset.id }))}
            value={draft.assetId}
            onValueChange={(value) => onChange({ assetId: value })}
          />
        </div>
        <div className="form-grid-two form-span-full">
          <label className="settings-field">
            <span>Start</span>
            <input type="datetime-local" value={draft.startTime} onChange={(event) => onChange({ startTime: event.target.value })} />
          </label>
          <label className="settings-field">
            <span>End</span>
            <input type="datetime-local" value={draft.endTime} onChange={(event) => onChange({ endTime: event.target.value })} />
          </label>
        </div>
        <label className="settings-field form-span-full">
          <span>Notes</span>
          <textarea className="settings-prompt small" value={draft.notes} onChange={(event) => onChange({ notes: event.target.value })} />
        </label>
        <div className="button-row form-span-full">
          <button className="button-primary" disabled={pending} type="submit">
            <AppIcon name={pending ? "spinner" : "save"} />
            Save run
          </button>
          <button disabled={pending} onClick={onCancel} type="button">Cancel</button>
          {error ? <span className="muted">{error}</span> : null}
        </div>
      </div>
    </form>
  );
}
