import { UserButton } from "@clerk/react";
import { useQuery } from "@tanstack/react-query";
import {
  createRootRoute,
  createRoute,
  createRouter,
  Link,
  Navigate,
  Outlet,
  useNavigate,
  useParams,
  useRouterState
} from "@tanstack/react-router";
import { useEffect, useState } from "react";

import { api } from "../api/client";
import { ArcLogo } from "../components/ArcLogo";
import { AppIcon } from "../components/AppIcon";
import { WorkspaceProgressScreen } from "../components/WorkspaceProgressScreen";
import { AssetsPage } from "./AssetsPage";
import { ChatPage } from "./ChatPage";
import { DataPage } from "./DataPage";
import { SettingsPage } from "./SettingsPage";
import { WorkbooksPage } from "./WorkbooksPage";
import { WorkspaceProvider } from "./workspaceContext";

type NavSection = "chat" | "assets" | "workbooks" | "data" | "settings";

const navItems = [
  { id: "chat", to: "/w/$workspaceId/chat", label: "Chat" },
  { id: "assets", to: "/w/$workspaceId/assets", label: "Assets" },
  { id: "workbooks", to: "/w/$workspaceId/workbooks", label: "Workbooks" },
  { id: "data", to: "/w/$workspaceId/data", label: "Data" }
] satisfies Array<{ id: NavSection; to: string; label: string }>;

const clerkEnabled = Boolean(import.meta.env.VITE_CLERK_PUBLISHABLE_KEY);
const settingsNavItem = {
  id: "settings",
  to: "/w/$workspaceId/settings",
  label: "Settings"
} satisfies { id: NavSection; to: string; label: string };

type ThemeMode = "light" | "dark";

function getInitialTheme(): ThemeMode {
  const storedTheme = window.localStorage.getItem("arc-theme");

  if (storedTheme === "light" || storedTheme === "dark") {
    return storedTheme;
  }

  return "light";
}

function Root() {
  return <Outlet />;
}

function WorkspaceRedirect() {
  const navigate = useNavigate();
  const workspaces = useQuery({ queryKey: ["workspaces"], queryFn: api.workspaces });

  useEffect(() => {
    if (!workspaces.data?.length) return;
    const lastWorkspaceId = window.localStorage.getItem("arc-workspace-id");
    const target =
      workspaces.data.find((workspace) => workspace.id === lastWorkspaceId) ?? workspaces.data[0];
    navigate({ to: "/w/$workspaceId", params: { workspaceId: target.id }, replace: true });
  }, [navigate, workspaces.data]);

  return (
    <WorkspaceProgressScreen
      error={workspaces.error instanceof Error ? workspaces.error.message : null}
    />
  );
}

function WorkspaceShell() {
  const params = useParams({ strict: false }) as { workspaceId?: string };
  const workspaceId = params.workspaceId ?? "";
  const pathname = useRouterState({ select: (state) => state.location.pathname });
  const activeSection = activeNavSection(pathname, workspaceId);
  const isChatRoute = activeSection === "chat";
  const navigate = useNavigate();
  const [theme, setTheme] = useState<ThemeMode>(getInitialTheme);
  const isDark = theme === "dark";
  const toggleLabel = isDark ? "Switch to light mode" : "Switch to dark mode";
  const toggleTitle = isDark ? "Dark mode on" : "Light mode on";
  const workspaces = useQuery({ queryKey: ["workspaces"], queryFn: api.workspaces });
  const workspaceOptions = workspaces.data ?? [];
  const workspaceExists = workspaceOptions.some((workspace) => workspace.id === workspaceId);
  const project = useQuery({
    queryKey: ["project", workspaceId],
    queryFn: () => api.project(workspaceId),
    enabled: Boolean(workspaceId)
  });
  const activeWorkspace =
    project.data?.workspace ?? workspaceOptions.find((workspace) => workspace.id === workspaceId);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem("arc-theme", theme);
  }, [theme]);

  useEffect(() => {
    if (workspaceId) window.localStorage.setItem("arc-workspace-id", workspaceId);
  }, [workspaceId]);

  useEffect(() => {
    if (!workspaceId || !workspaceOptions.length || workspaceExists) return;
    navigate({
      to: "/w/$workspaceId",
      params: { workspaceId: workspaceOptions[0].id },
      replace: true
    });
  }, [navigate, workspaceExists, workspaceId, workspaceOptions]);

  return (
    <WorkspaceProvider value={{ workspaceId, workspace: activeWorkspace }}>
      <div className={isChatRoute ? "app-shell chat-shell" : "app-shell"}>
        <header className="top-nav">
          <Link to="/w/$workspaceId" params={{ workspaceId }} className="top-nav-brand" aria-label="Arc home">
            <ArcLogo />
          </Link>
          <nav className="top-nav-tabs" aria-label="Primary navigation">
            {navItems.map((item) => (
              <Link
                to={item.to}
                params={{ workspaceId }}
                className={activeSection === item.id ? "top-nav-tab active" : "top-nav-tab"}
                key={item.to}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <div className="top-nav-actions">
            <button
              className="button button-icon theme-toggle"
              type="button"
              onClick={() => setTheme(isDark ? "light" : "dark")}
              aria-label={toggleLabel}
              aria-pressed={isDark}
              data-theme-mode={isDark ? "dark" : "light"}
              title={toggleTitle}
            >
              <AppIcon name={isDark ? "sun" : "moon"} />
            </button>
            <Link
              to={settingsNavItem.to}
              params={{ workspaceId }}
              className={
                activeSection === settingsNavItem.id
                  ? "button button-icon top-nav-icon-link active"
                  : "button button-icon top-nav-icon-link"
              }
              aria-label={settingsNavItem.label}
              title={settingsNavItem.label}
            >
              <AppIcon name="settings" />
            </Link>
            {clerkEnabled ? <UserButton /> : null}
          </div>
        </header>
        <main className="main">
          <Outlet />
        </main>
      </div>
    </WorkspaceProvider>
  );
}

function WorkspaceChatRedirect() {
  const { workspaceId } = useParams({ from: workspaceRoute.id });

  return (
    <Navigate
      to="/w/$workspaceId/chat"
      params={{ workspaceId }}
      replace
    />
  );
}

function activeNavSection(pathname: string, workspaceId: string): NavSection {
  const workspaceRoot = `/w/${workspaceId}`;
  const path = pathname === workspaceRoot ? "/" : pathname.slice(workspaceRoot.length) || "/";

  if (path === "/chat" || path.startsWith("/chat/")) return "chat";
  if (path === "/assets" || path.startsWith("/assets/")) return "assets";
  if (path === "/workbooks" || path.startsWith("/workbooks/")) return "workbooks";
  if (path === "/data" || path.startsWith("/data/")) return "data";
  if (path === "/settings" || path.startsWith("/settings/")) return "settings";

  return "chat";
}

const rootRoute = createRootRoute({ component: Root });

const workspaceHomeRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: WorkspaceRedirect
});

const workspaceRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/w/$workspaceId",
  component: WorkspaceShell
});

const assetsRoute = createRoute({
  getParentRoute: () => workspaceRoute,
  path: "/assets",
  component: AssetsPage
});

const workspaceChatRedirectRoute = createRoute({
  getParentRoute: () => workspaceRoute,
  path: "/",
  component: WorkspaceChatRedirect
});

const assetDetailRoute = createRoute({
  getParentRoute: () => workspaceRoute,
  path: "/assets/$assetId",
  component: AssetsPage
});

const chatRoute = createRoute({
  getParentRoute: () => workspaceRoute,
  path: "/chat",
  component: ChatPage
});

const dataRoute = createRoute({
  getParentRoute: () => workspaceRoute,
  path: "/data",
  component: DataPage
});

const workbooksRoute = createRoute({
  getParentRoute: () => workspaceRoute,
  path: "/workbooks",
  component: WorkbooksPage
});

const workbookDetailRoute = createRoute({
  getParentRoute: () => workspaceRoute,
  path: "/workbooks/$workbookId",
  component: WorkbooksPage
});

const settingsRoute = createRoute({
  getParentRoute: () => workspaceRoute,
  path: "/settings",
  component: SettingsPage
});

const routeTree = rootRoute.addChildren([
  workspaceHomeRoute,
  workspaceRoute.addChildren([
    workspaceChatRedirectRoute,
    assetsRoute,
    assetDetailRoute,
    workbooksRoute,
    workbookDetailRoute,
    chatRoute,
    dataRoute,
    settingsRoute
  ])
]);

export const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
