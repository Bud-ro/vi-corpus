from __future__ import annotations

import json
from pathlib import Path

from app.core import execution_outputs


def test_legacy_none_check_severity_is_treated_as_unset(tmp_path: Path) -> None:
    execution_dir = tmp_path / "execution"
    outputs_dir = execution_dir / "outputs"
    outputs_dir.mkdir(parents=True)
    (outputs_dir / "summary.json").write_text(
        json.dumps(
            {
                "checks": [
                    {
                        "id": "signal-quality",
                        "name": "Signal quality",
                        "status": "pass",
                        "severity": "none",
                        "message": "No issues found.",
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )

    checks = execution_outputs.read_check_results(execution_dir)

    assert checks[0].severity is None
    assert execution_outputs.check_counts(execution_dir) == {"pass": 1, "warn": 0, "fail": 0}
