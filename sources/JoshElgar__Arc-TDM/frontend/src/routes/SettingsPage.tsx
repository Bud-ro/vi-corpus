import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { FormEvent } from "react";
import { useEffect, useState } from "react";

import { api } from "../api/client";
import type { ProjectSettings } from "../api/types";
import { AppIcon } from "../components/AppIcon";
import { PageLoading } from "../components/PageLoading";
import { PageHeader } from "../components/PageHeader";
import { useWorkspaceId } from "./workspaceContext";

const emptySettings: ProjectSettings = {
  name: "",
  agent_system_prompt: ""
};

const protectedSettingsPassword = "CEDRICTUBMAN";

export function SettingsPage() {
  const workspaceId = useWorkspaceId();
  const queryClient = useQueryClient();
  const settings = useQuery({ queryKey: ["settings", workspaceId], queryFn: () => api.settings(workspaceId) });
  const apiToken = useQuery({
    queryKey: ["workspace-api-token", workspaceId],
    queryFn: () => api.workspaceApiToken(workspaceId)
  });
  const [draft, setDraft] = useState<ProjectSettings>(emptySettings);
  const [createdToken, setCreatedToken] = useState("");
  const [tokenCopied, setTokenCopied] = useState(false);
  const [workspaceIdCopied, setWorkspaceIdCopied] = useState(false);
  const [protectedSettingsInput, setProtectedSettingsInput] = useState("");
  const [showSaved, setShowSaved] = useState(false);
  const protectedSettingsUnlocked = protectedSettingsInput === protectedSettingsPassword;
  const save = useMutation({
    mutationFn: (settings: ProjectSettings) => api.saveSettings(workspaceId, settings),
    onSuccess: (saved) => {
      setDraft(saved);
      setShowSaved(true);
      queryClient.invalidateQueries({ queryKey: ["settings", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["project", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workspaces"] });
      queryClient.invalidateQueries({ queryKey: ["assets", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["charts", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["reports", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["runs", workspaceId] });
    },
    onError: () => {
      setShowSaved(false);
    }
  });
  const generateApiToken = useMutation({
    mutationFn: () => api.generateWorkspaceApiToken(workspaceId),
    onSuccess: (created) => {
      setCreatedToken(created.token);
      setTokenCopied(false);
      queryClient.invalidateQueries({ queryKey: ["workspace-api-token", workspaceId] });
    }
  });
  const deleteApiToken = useMutation({
    mutationFn: () => api.deleteWorkspaceApiToken(workspaceId),
    onSuccess: () => {
      setCreatedToken("");
      setTokenCopied(false);
      queryClient.invalidateQueries({ queryKey: ["workspace-api-token", workspaceId] });
    }
  });

  useEffect(() => {
    if (settings.data) setDraft(settings.data);
  }, [settings.data]);

  useEffect(() => {
    setWorkspaceIdCopied(false);
  }, [workspaceId]);

  useEffect(() => {
    if (!showSaved) return;

    const timeout = window.setTimeout(() => setShowSaved(false), 3000);
    return () => window.clearTimeout(timeout);
  }, [showSaved]);

  function updateDraft(patch: Partial<ProjectSettings>) {
    setShowSaved(false);
    setDraft((current) => ({ ...current, ...patch }));
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setShowSaved(false);
    save.mutate(draft);
  }

  function copyCreatedToken() {
    if (!createdToken) return;
    navigator.clipboard?.writeText(createdToken).then(() => setTokenCopied(true));
  }

  function copyWorkspaceId() {
    navigator.clipboard?.writeText(workspaceId).then(() => setWorkspaceIdCopied(true));
  }

  if (settings.isLoading) {
    return <PageLoading label="Loading settings" />;
  }

  return (
    <div className="page settings-page">
      <PageHeader title="Settings" />
      <form className="settings-panel" onSubmit={submit}>
        <label className="settings-field">
          <span>Workspace name</span>
          <input
            value={draft.name}
            onChange={(event) => updateDraft({ name: event.target.value })}
          />
        </label>

        <div className="settings-field">
          <span>Workspace id</span>
          <div className="settings-copy-row">
            <input aria-label="Workspace id" readOnly value={workspaceId} />
            <button onClick={copyWorkspaceId} type="button">
              <AppIcon name={workspaceIdCopied ? "check" : "copy"} />
              {workspaceIdCopied ? "Copied" : "Copy"}
            </button>
          </div>
        </div>

        <div className="settings-field">
          <span>Workspace access token</span>
          <div className="api-token-panel">
            <div className="api-token-status">
              {apiToken.data?.token_prefix ? (
                <code>{apiToken.data.token_prefix}...</code>
              ) : (
                <span className="muted">No token</span>
              )}
              {apiToken.data?.created_at ? (
                <span className="muted">Created {formatDate(apiToken.data.created_at)}</span>
              ) : null}
              {apiToken.data?.last_used_at ? (
                <span className="muted">Last used {formatDate(apiToken.data.last_used_at)}</span>
              ) : null}
            </div>
            <div className="button-row">
              <button disabled={generateApiToken.isPending || apiToken.isLoading} onClick={() => generateApiToken.mutate()} type="button">
                <AppIcon name={generateApiToken.isPending ? "spinner" : "refresh"} />
                {apiToken.data?.token_prefix ? "Regenerate" : "Generate"}
              </button>
              {apiToken.data?.token_prefix ? (
                <button disabled={deleteApiToken.isPending} onClick={() => deleteApiToken.mutate()} type="button">
                  <AppIcon name={deleteApiToken.isPending ? "spinner" : "trash"} />
                  Revoke
                </button>
              ) : null}
            </div>
            {createdToken ? (
              <div className="api-token-created">
                <input aria-label="New workspace access token" readOnly value={createdToken} />
                <button onClick={copyCreatedToken} type="button">
                  <AppIcon name={tokenCopied ? "check" : "copy"} />
                  {tokenCopied ? "Copied" : "Copy"}
                </button>
              </div>
            ) : null}
            {generateApiToken.isError ? <span className="muted">{generateApiToken.error.message}</span> : null}
            {deleteApiToken.isError ? <span className="muted">{deleteApiToken.error.message}</span> : null}
          </div>
        </div>

        {protectedSettingsUnlocked ? (
          <>
            <label className="settings-field">
              <span>Arc Agent system prompt</span>
              <textarea
                className="settings-prompt"
                value={draft.agent_system_prompt}
                onChange={(event) => updateDraft({ agent_system_prompt: event.target.value })}
              />
            </label>
          </>
        ) : (
          <label className="settings-field settings-password-field">
            <span>Protected settings</span>
            <input
              autoComplete="off"
              onChange={(event) => setProtectedSettingsInput(event.target.value)}
              placeholder="Password"
              type="password"
              value={protectedSettingsInput}
            />
          </label>
        )}

        <div className="button-row">
          <button disabled={save.isPending || settings.isLoading} type="submit">
            <AppIcon name={save.isPending ? "spinner" : "save"} />
            Save
          </button>
          {showSaved ? (
            <span className="settings-save-status" role="status">
              Saved
            </span>
          ) : null}
          {save.isError ? <span className="muted">{save.error.message}</span> : null}
        </div>
      </form>
    </div>
  );
}

function formatDate(value: string) {
  return new Date(value).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short"
  });
}
