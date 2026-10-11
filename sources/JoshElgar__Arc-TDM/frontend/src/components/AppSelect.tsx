import { Select } from "@base-ui/react/select";

import { AppIcon } from "./AppIcon";

type AppSelectOption = {
  disabled?: boolean;
  label: string;
  value: string;
};

type AppSelectGroup = {
  label: string;
  options: AppSelectOption[];
};

type AppSelectProps = {
  ariaLabel: string;
  disabled?: boolean;
  groups?: AppSelectGroup[];
  isLoading?: boolean;
  options: AppSelectOption[];
  value: string;
  onValueChange: (value: string) => void;
};

export function AppSelect({
  ariaLabel,
  disabled = false,
  groups,
  isLoading = false,
  options,
  value,
  onValueChange
}: AppSelectProps) {
  const rootOptions = groups?.flatMap((group) => group.options) ?? options;

  return (
    <Select.Root
      disabled={disabled || isLoading}
      items={rootOptions}
      value={isLoading ? null : value}
      onValueChange={(nextValue) => {
        if (nextValue) onValueChange(nextValue);
      }}
    >
      <Select.Trigger className="app-select-trigger" aria-label={ariaLabel}>
        {isLoading ? (
          <span aria-hidden="true" className="thinking-dots app-select-loading">
            <span />
            <span />
            <span />
          </span>
        ) : (
          <Select.Value />
        )}
        <Select.Icon>
          <AppIcon name="chevronDown" size={14} />
        </Select.Icon>
      </Select.Trigger>
      <Select.Portal>
        <Select.Positioner
          align="start"
          alignItemWithTrigger={false}
          className="app-select-positioner"
          collisionAvoidance={{ side: "shift", align: "shift", fallbackAxisSide: "none" }}
          collisionPadding={8}
          sideOffset={4}
        >
          <Select.Popup className="app-select-content">
            <Select.List>
              {groups
                ? groups.map((group) => (
                    <Select.Group className="app-select-group" key={group.label}>
                      <Select.GroupLabel className="app-select-group-label">{group.label}</Select.GroupLabel>
                      {group.options.map((option) => renderOption(option))}
                    </Select.Group>
                  ))
                : options.map((option) => renderOption(option))}
            </Select.List>
          </Select.Popup>
        </Select.Positioner>
      </Select.Portal>
    </Select.Root>
  );
}

function renderOption(option: AppSelectOption) {
  return (
    <Select.Item
      className="app-select-item"
      disabled={option.disabled}
      key={option.value}
      value={option.value}
    >
      <Select.ItemText>{option.label}</Select.ItemText>
      <Select.ItemIndicator className="app-select-item-indicator">
        <AppIcon name="check" size={13} />
      </Select.ItemIndicator>
    </Select.Item>
  );
}
