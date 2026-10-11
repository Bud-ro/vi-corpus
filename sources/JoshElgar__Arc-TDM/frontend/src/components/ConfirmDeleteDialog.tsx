import type React from "react";
import { Dialog } from "@base-ui/react/dialog";

import { AppIcon, type AppIconName } from "./AppIcon";

type ConfirmDeleteDialogProps = {
  title: string;
  children: React.ReactNode;
  confirmIcon?: AppIconName;
  confirmLabel?: string;
  error?: string | null;
  isPending?: boolean;
  onCancel: () => void;
  onConfirm: () => void;
};

export function ConfirmDeleteDialog({
  title,
  children,
  confirmIcon = "trash",
  confirmLabel = "Delete",
  error,
  isPending = false,
  onCancel,
  onConfirm
}: ConfirmDeleteDialogProps) {
  return (
    <Dialog.Root open onOpenChange={(open) => !open && onCancel()}>
      <Dialog.Portal>
        <Dialog.Backdrop className="dialog-backdrop" />
        <Dialog.Popup className="confirm-dialog">
          <div className="confirm-dialog-heading">
            <Dialog.Title>{title}</Dialog.Title>
            <Dialog.Close
              render={
                <button aria-label="Close dialog" className="button button-icon" type="button">
                  <AppIcon name="cross" />
                </button>
              }
            />
          </div>
          <div className="confirm-dialog-body">{children}</div>
          {error ? <p className="inline-error confirm-error">{error}</p> : null}
          <div className="confirm-dialog-actions">
            <Dialog.Close
              render={
                <button type="button">
                  Cancel
                </button>
              }
            />
            <button className="button button-danger" disabled={isPending} type="button" onClick={onConfirm}>
              <AppIcon name={isPending ? "spinner" : confirmIcon} />
              {confirmLabel}
            </button>
          </div>
        </Dialog.Popup>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
