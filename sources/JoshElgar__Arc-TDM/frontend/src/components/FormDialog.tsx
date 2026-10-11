import type React from "react";
import { Dialog } from "@base-ui/react/dialog";

import { AppIcon } from "./AppIcon";

type FormDialogProps = {
  children: React.ReactNode;
  className?: string;
  onClose: () => void;
  title: string;
};

export function FormDialog({ children, className, onClose, title }: FormDialogProps) {
  const popupClassName = ["form-dialog", className].filter(Boolean).join(" ");

  return (
    <Dialog.Root open onOpenChange={(open) => !open && onClose()}>
      <Dialog.Portal>
        <Dialog.Backdrop className="dialog-backdrop" />
        <Dialog.Popup className={popupClassName}>
          <div className="form-dialog-heading">
            <Dialog.Title>{title}</Dialog.Title>
            <Dialog.Close
              render={
                <button aria-label="Close dialog" className="button button-icon" type="button">
                  <AppIcon name="cross" />
                </button>
              }
            />
          </div>
          <div className="form-dialog-body">{children}</div>
        </Dialog.Popup>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
