import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { api } from "../api/client";
import { AppIcon } from "./AppIcon";
import { ConfirmDeleteDialog } from "./ConfirmDeleteDialog";
import { useWorkspaceId } from "../routes/workspaceContext";

export function GitStatusPanel() {
  const workspaceId = useWorkspaceId();
  const queryClient = useQueryClient();
  const [message, setMessage] = useState("Update workspace");
  const [discardOpen, setDiscardOpen] = useState(false);
  const status = useQuery({ queryKey: ["git-status", workspaceId], queryFn: () => api.gitStatus(workspaceId) });
  const commit = useMutation({
    mutationFn: (message: string) => api.commit(workspaceId, message),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] })
  });
  const discard = useMutation({
    mutationFn: () => api.discardTracked(workspaceId),
    onSuccess: () => {
      setDiscardOpen(false);
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });

  return (
    <section className="panel compact">
      {discardOpen ? (
        <ConfirmDeleteDialog
          confirmIcon="undo"
          confirmLabel="Discard"
          error={discard.error instanceof Error ? discard.error.message : null}
          isPending={discard.isPending}
          title="Discard tracked changes?"
          onCancel={() => setDiscardOpen(false)}
          onConfirm={() => discard.mutate()}
        >
          <div className="delete-copy">
            <p>Tracked workspace changes will be discarded. Untracked files will be kept.</p>
          </div>
        </ConfirmDeleteDialog>
      ) : null}
      <div className="panel-title">
        <span>Workspace git</span>
        <button className="button button-icon" onClick={() => status.refetch()} title="Refresh status">
          <AppIcon name={status.isFetching ? "spinner" : "refresh"} />
        </button>
      </div>
      <div className="meta-row">
        <span>Branch</span>
        <strong>{status.data?.branch ?? "..."}</strong>
      </div>
      <div className="status-list">
        {status.data?.porcelain.length ? (
          status.data.porcelain.slice(0, 6).map((line) => <code key={line}>{line}</code>)
        ) : (
          <span className="muted">No visible changes</span>
        )}
      </div>
      <div className="commit-row">
        <input value={message} onChange={(event) => setMessage(event.target.value)} />
        <button onClick={() => commit.mutate(message)} disabled={commit.isPending}>
          <AppIcon name={commit.isPending ? "spinner" : "gitCommit"} />
          Commit
        </button>
      </div>
      <button
        className="button button-secondary button-block git-discard-action"
        onClick={() => {
          discard.reset();
          setDiscardOpen(true);
        }}
        disabled={discard.isPending}
      >
        <AppIcon name={discard.isPending ? "spinner" : "undo"} />
        Discard tracked
      </button>
    </section>
  );
}
