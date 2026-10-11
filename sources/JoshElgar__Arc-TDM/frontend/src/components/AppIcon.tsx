import { icons as proIcons } from "@iconify-json/proicons";
import { Icon, addCollection } from "@iconify/react";
import type { ComponentProps } from "react";

addCollection(proIcons);

const appIcons = {
  arrowDown: "arrow-down",
  arrowUp: "arrow-up",
  chat: "chat",
  check: "checkmark",
  chevronDown: "chevron-down",
  chevronLeft: "chevron-left",
  chevronRight: "chevron-right",
  clock: "clock",
  copy: "copy",
  cross: "cancel",
  dashboard: "grid",
  data: "database",
  dot: "circle-small",
  edit: "edit",
  file: "file",
  folder: "folder",
  gitBranch: "branch-fork",
  gitCommit: "git-commit",
  home: "home",
  link: "link",
  moon: "moon",
  more: "more",
  play: "play",
  plus: "add",
  refresh: "arrow-sync",
  reports: "file-text",
  review: "eye",
  save: "save",
  search: "search",
  send: "send",
  settings: "settings",
  spinner: "spinner",
  steps: "task-list",
  sun: "brightness",
  trash: "delete",
  undo: "arrow-undo",
  upload: "arrow-upload",
  charts: "bar-chart"
} as const;

export type AppIconName = keyof typeof appIcons;

type AppIconProps = Omit<ComponentProps<typeof Icon>, "icon" | "height" | "width"> & {
  name: AppIconName;
  size?: number;
};

export function AppIcon({ name, size = 16, className, ...props }: AppIconProps) {
  const iconClassName = ["app-icon", name === "spinner" ? "is-spinning" : "", className]
    .filter(Boolean)
    .join(" ");

  return (
    <Icon
      aria-hidden="true"
      className={iconClassName}
      focusable="false"
      height={size}
      icon={`proicons:${appIcons[name]}`}
      width={size}
      {...props}
    />
  );
}
