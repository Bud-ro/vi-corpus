import { Progress } from "@base-ui/react/progress";
import { useEffect, useState } from "react";

import { ArcLogo } from "./ArcLogo";

const progressDurationMs = 15_000;

export function WorkspaceProgressScreen({ error }: { error?: string | null }) {
  const progress = useTimedProgress(!error);

  return (
    <main className="workspace-start">
      <div className="workspace-start-panel">
        <div className="brand-copy">
          <ArcLogo />
        </div>
        <Progress.Root
          aria-label="Preparing workspace"
          className="workspace-progress-root"
          value={progress}
        >
          <Progress.Track className="workspace-progress-track">
            <Progress.Indicator
              className="workspace-progress-indicator"
              style={{ transform: `scaleX(${progress / 100})` }}
            />
          </Progress.Track>
        </Progress.Root>
        {error ? <p className="inline-error workspace-progress-error">{error}</p> : null}
      </div>
    </main>
  );
}

function useTimedProgress(active: boolean) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (!active) {
      setProgress(100);
      return;
    }

    let frameId = 0;
    const startedAt = performance.now();

    function tick() {
      const elapsed = performance.now() - startedAt;
      setProgress(Math.min(100, Math.round((elapsed / progressDurationMs) * 100)));
      if (elapsed < progressDurationMs) {
        frameId = requestAnimationFrame(tick);
      }
    }

    frameId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frameId);
  }, [active]);

  return progress;
}
