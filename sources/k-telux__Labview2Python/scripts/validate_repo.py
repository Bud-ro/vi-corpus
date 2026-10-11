from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "labview-to-python-industrial" / "SKILL.md"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    required = [
        SKILL,
        ROOT / "skills" / "labview-to-python-industrial" / "LICENSE.txt",
        ROOT / "skills" / "labview-to-python-industrial" / "agents" / "openai.yaml",
        ROOT / "rules" / "labview-to-python-industrial.md",
        ROOT / "README.zh-CN.md",
        ROOT / "README.ja.md",
        ROOT / "examples" / "README.md",
        ROOT / "examples" / "showcase" / "README.md",
        ROOT / "examples" / "showcase" / "assets" / "pump-probe-industrial-ui.png",
        ROOT / "examples" / "showcase" / "assets" / "spectroscopy-tcspc-ui.png",
    ]
    for path in required:
        check(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", errors)

    skill_files = list((ROOT / "skills").rglob("SKILL.md"))
    check(skill_files == [SKILL], "expected exactly one canonical SKILL.md", errors)

    if SKILL.is_file():
        text = SKILL.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        check(len(parts) == 3 and not parts[0].strip(), "invalid SKILL frontmatter", errors)
        if len(parts) == 3:
            fields = {}
            for line in parts[1].splitlines():
                if line.strip() and ":" in line:
                    key, value = line.split(":", 1)
                    fields[key.strip()] = value.strip()
            check({"name", "description"} <= set(fields), "frontmatter requires name and description", errors)
            check(fields.get("name") == SKILL.parent.name, "skill name must match directory", errors)
            check(len(fields.get("description", "")) >= 100, "skill description is too narrow", errors)
            for ref in re.findall(r"`(references/[^`]+\.md)`", parts[2]):
                check((SKILL.parent / ref).is_file(), f"missing referenced file: {ref}", errors)

    canonical_rule = ROOT / "rules" / "labview-to-python-industrial.md"
    for path in [
        canonical_rule,
        ROOT / "rules" / "labview-to-python-industrial.zh-CN.md",
        ROOT / "rules" / "labview-to-python-industrial.ja-JP.md",
    ]:
        if path.is_file():
            check(VERSION in path.read_text(encoding="utf-8"), f"rule version drift: {path.name}", errors)

    for slug in [
        "01-dual-project-orchestration",
        "02-performance-heatmap-gate",
        "03-packaged-exe-gate",
    ]:
        for name in ["input.md", "output.md"]:
            check((ROOT / "examples" / slug / name).is_file(), f"missing example: {slug}/{name}", errors)

    evals_path = SKILL.parent / "evals" / "evals.json"
    check(evals_path.is_file(), "missing skill evals/evals.json", errors)
    if evals_path.is_file():
        try:
            evals = json.loads(evals_path.read_text(encoding="utf-8"))
            check(isinstance(evals, list) and len(evals) >= 3, "expected at least three eval cases", errors)
            check(all(case.get("expected_skill") == "labview-to-python-industrial" for case in evals), "eval routing drift", errors)
        except (json.JSONDecodeError, AttributeError) as exc:
            errors.append(f"invalid evals JSON: {exc}")

    for path in ROOT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        check("C:\\Users\\" not in content, f"private Windows path in {path.relative_to(ROOT)}", errors)
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if relative:
                check((path.parent / relative).exists(), f"broken link in {path.relative_to(ROOT)}: {target}", errors)

    for name in ["pump-probe-industrial-ui.png", "spectroscopy-tcspc-ui.png"]:
        path = ROOT / "examples" / "showcase" / "assets" / name
        if path.is_file():
            payload = path.read_bytes()
            check(payload[:8] == b"\x89PNG\r\n\x1a\n", f"invalid PNG: {name}", errors)
            width = int.from_bytes(payload[16:20], "big")
            height = int.from_bytes(payload[20:24], "big")
            check(width >= 1200 and height >= 700, f"showcase image is too small: {name} ({width}x{height})", errors)
            check(path.stat().st_size < 1_000_000, f"showcase image is too large: {name}", errors)

    if errors:
        print("validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"repository valid: labview-to-python-industrial v{VERSION}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
