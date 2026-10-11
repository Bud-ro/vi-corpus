import { createContext, useContext } from "react";

import type { WorkspaceSummary } from "../api/types";

type WorkspaceContextValue = {
  workspaceId: string;
  workspace?: WorkspaceSummary;
};

const WorkspaceContext = createContext<WorkspaceContextValue | null>(null);

export const WorkspaceProvider = WorkspaceContext.Provider;

export function useWorkspace() {
  const value = useContext(WorkspaceContext);
  if (!value) throw new Error("useWorkspace must be used inside a workspace route.");
  return value;
}

export function useWorkspaceId() {
  return useWorkspace().workspaceId;
}
