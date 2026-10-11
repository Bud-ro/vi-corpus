# Contributing

Contributions that improve migration safety, evidence quality, hardware boundary
clarity, industrial UI usability, or cross-agent portability are welcome.

## Before Opening A Pull Request

1. Keep `skills/labview-to-python-industrial/SKILL.md` concise and route detail to
   a directly linked reference.
2. Keep the English `SKILL.md` canonical. Update the derived rule and localized
   summaries when its meaning changes.
3. Do not weaken independent statuses for source UI, simulator, packaged EXE,
   real hardware, or unresolved subsystems.
4. Add or update a sanitized input/output example for a new workflow rule.
5. Run `python scripts/validate_repo.py`.

## Evidence Requirements

Behavioral claims should identify the source artifact, actual interaction path,
and acceptance boundary. UI contributions need target-window screenshots from a
real interaction. Hardware claims need real device evidence; simulator evidence
must remain labeled as simulation.

## Prohibited Content

Do not commit credentials, private laboratory data, identifiable local paths,
vendor license files, or SDK binaries without explicit redistribution rights.

Use a focused branch and pull request. Explain the problem, why the rule belongs
in a reusable skill, and how it was validated.
