from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ModuleNotFoundError:  # Keep this script runnable with plain system Python.
    yaml = None

from check_stickers import sticker_issues

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPORT = DOCS / "_site_health.md"
MKDOCS = ROOT / "mkdocs.yml"
PEOPLE_DATA = DOCS / "_data" / "people.yml"
REQUIRED = ["docs/index.md", "docs/olc-example.md", "docs/example.md", "mkdocs.yml", "README.md", "AGENTS.md", "PROMPT_ACTION_LOG.md",
            "docs/stylesheets/tokens.css", "docs/stylesheets/extra.css",
            "docs/javascripts/presentation-mode.js", "docs/instructions/day1.md",
            "docs/instructions/day2.md", "docs/instructions/stewardship.md",
            "docs/instructions/cubedynamics.md", "docs/facilitator-guide.md",
            "docs/people/template.md", "docs/storage/add-your-profile.md",
            "docs/references.bib", "docs/_data/people.yml"]
ASSET_DIRS = ["docs/assets/hero", "docs/assets/whiteboards", "docs/assets/explorations",
              "docs/assets/figures", "docs/assets/team", "docs/assets/files",
              "docs/assets/stickers", "docs/assets/people"]
PLACEHOLDERS = ["[link]", "TODO", "TBD", "CHANGE_ME", "REPLACE_ME"]
NAV_ITEMS = ["Home", "OLC Example", "Fire Example", "Directions", "Facilitator Guide",
             "Cloud Triangle", "Links"]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ACTIVE_SCHEDULE_FILES = [
    "docs/index.md",
    "docs/instructions.md",
    "docs/instructions/day1.md",
    "docs/instructions/day2.md",
    "docs/project_template.md",
]
STALE_SCHEDULE_PATTERNS = [
    (re.compile(r"\b3[- ]Day\b", re.I), "three-day event language"),
    (re.compile(r"\bDay 3\b", re.I), "active Day 3 language"),
    (re.compile(r"\b(?:2|6)[- ]minute (?:report|walkthrough)", re.I), "retired fixed report timing"),
]


def nav_labels(text: str) -> list[str]:
    labels, in_nav = [], False
    for line in text.splitlines():
        if not in_nav:
            in_nav = line.strip() == "nav:"
            continue
        if line and not line.startswith((" ", "\t", "-")):
            break
        match = re.match(r"^\s{2}-\s+([^:]+):\s*", line)
        if match:
            labels.append(match.group(1).strip())
    return labels


def text_files() -> list[Path]:
    docs_files = [path for path in sorted(DOCS.rglob("*.md")) if path.name != "_site_health.md"]
    return [ROOT / "README.md", MKDOCS] + docs_files


def missing_file_issues() -> list[str]:
    return [f"⚠ Missing required file: {path}" for path in REQUIRED if not (ROOT / path).exists()]


def missing_asset_dir_issues() -> list[str]:
    return [f"⚠ Missing asset folder: {path}" for path in ASSET_DIRS if not (ROOT / path).is_dir()]


def placeholder_issues() -> list[str]:
    issues = []
    for path in text_files():
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in PLACEHOLDERS:
            if needle in text:
                issues.append(f"⚠ Placeholder detected: {needle} in {path.relative_to(ROOT)}")
    return issues


def navigation_issues() -> list[str]:
    labels = nav_labels(MKDOCS.read_text(encoding="utf-8")) if MKDOCS.exists() else []
    return [f"⚠ Navigation issue: missing nav item '{item}' in mkdocs.yml" for item in NAV_ITEMS if item not in labels]


def schedule_issues() -> list[str]:
    issues: list[str] = []
    for relative_path in ACTIVE_SCHEDULE_FILES:
        path = ROOT / relative_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern, label in STALE_SCHEDULE_PATTERNS:
            if pattern.search(text):
                issues.append(f"⚠ Schedule issue: {label} in {relative_path}")
    return issues


def sticker_validation_issues() -> list[str]:
    return [
        f"⚠ Sticker navigation issue: {issue}"
        for issue in sticker_issues()
    ]


def is_external_or_anchor(raw: str) -> bool:
    return raw.startswith(("http://", "https://", "mailto:", "#"))


def resolve_docs_target(raw: str) -> Path | None:
    target = unquote(raw.strip().strip("<>").split("#", 1)[0].split("?", 1)[0])
    if not target or is_external_or_anchor(target) or target.startswith("/"):
        return None
    if target.startswith("../"):
        return (PEOPLE_DATA.parent / target).resolve()
    return (DOCS / target).resolve()


def parse_simple_people_yaml(text: str) -> list[dict[str, object]]:
    people: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_list_key: str | None = None
    in_people = False

    for line in text.splitlines():
        raw = line.rstrip()
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "people:":
            in_people = True
            continue
        if not in_people:
            continue
        if raw.startswith("  - "):
            current = {}
            people.append(current)
            current_list_key = None
            remainder = raw[4:].strip()
            if ":" in remainder:
                key, value = remainder.split(":", 1)
                current[key.strip()] = value.strip()
            continue
        if current is None:
            continue
        if raw.startswith("    - ") and current_list_key:
            current.setdefault(current_list_key, [])
            value = raw[6:].strip()
            if isinstance(current[current_list_key], list) and value:
                current[current_list_key].append(value)
            continue
        if raw.startswith("    ") and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                current[key] = value
                current_list_key = None
            else:
                current[key] = []
                current_list_key = key

    return people


def people_gallery_issues() -> list[str]:
    if not PEOPLE_DATA.exists():
        return [f"⚠ People gallery issue: missing {PEOPLE_DATA.relative_to(ROOT)}"]

    text = PEOPLE_DATA.read_text(encoding="utf-8")
    if yaml is not None:
        try:
            data = yaml.safe_load(text) or {}
        except yaml.YAMLError as exc:
            return [f"⚠ People gallery issue: {PEOPLE_DATA.relative_to(ROOT)} is not valid YAML ({exc})"]
    else:
        data = {"people": parse_simple_people_yaml(text)}

    people = data.get("people", [])
    if not isinstance(people, list):
        return [f"⚠ People gallery issue: {PEOPLE_DATA.relative_to(ROOT)} should contain a `people:` list"]

    issues: list[str] = []
    for index, person in enumerate(people, start=1):
        if not isinstance(person, dict):
            issues.append(f"⚠ People gallery issue: entry {index} should be a YAML mapping")
            continue

        profile = str(person.get("profile", "") or "").strip()
        if not profile:
            issues.append(f"⚠ People gallery issue: entry {index} should use `profile: people/first-last.md`")
            continue

        if any(key in person for key in ["name", "summary", "skills", "interests", "focus", "brings", "profile_url"]):
            issues.append(f"⚠ People gallery issue: entry {index} should keep profile text in Markdown, not people.yml")

        profile_path = resolve_docs_target(profile)
        if profile_path is not None and not profile_path.is_file():
            issues.append(f"⚠ People gallery issue: profile file does not exist: {profile}")
            continue

        if profile_path is not None and profile_path.is_file():
            profile_text = profile_path.read_text(encoding="utf-8")
            if not profile_text.startswith("---\n"):
                issues.append(f"⚠ People gallery issue: {profile} should start with YAML front matter")

    return issues


def internal_link_issues() -> list[str]:
    issues = []
    for path in [p for p in sorted(DOCS.rglob("*.md")) if p.name != "_site_health.md"]:
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"`[^`]+`", "", text)
        for raw in LINK_RE.findall(text):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                issues.append(f"⚠ Internal link issue: {path.relative_to(ROOT)} links to missing target '{raw}'")
    return issues


def completion_checks() -> list[tuple[bool, str, str]]:
    """Return non-blocking Home-page editing checks with plain-language guidance."""
    if not (DOCS / "index.md").exists():
        return [(False, "Home page exists", "Restore `docs/index.md` before editing the project story.")]

    text = (DOCS / "index.md").read_text(encoding="utf-8")
    return [
        (
            "# Team Project: Make This Your Own" not in text,
            "Project title is customized",
            "Replace the default H1 and front-matter title with the team’s project name.",
        ),
        (
            "Our working question:\n\n..." not in text,
            "Working question is written",
            "State one question narrow enough to investigate during the event.",
        ),
        (
            "| ... | ... | ... | ... | ... |" not in text,
            "Main evidence is documented",
            "Complete the Data and Evidence row: dataset, source, place, period, and meaning.",
        ),
        (
            "- **Main artifact:** ..." not in text,
            "Main artifact is linked",
            "Link a figure, map, notebook, workflow, prototype, resource, or documented attempt.",
        ),
        (
            "**Observation — what happened:** ..." not in text
            and "**Evidence — what supports it:** ..." not in text
            and "**Interpretation — what we think it means:** ..." not in text,
            "Learning separates observation, evidence, and interpretation",
            "Replace all three prompts and point the claim to a visible artifact.",
        ),
        (
            "What these data or artifacts cannot tell us:\n\n..." not in text,
            "Evidence boundary is stated",
            "Name the most important uncertainty or claim the evidence cannot support.",
        ),
        (
            "Next technical step:\n\n..." not in text
            and "Next stewardship or collaboration step:\n\n..." not in text,
            "Technical and stewardship next steps are written",
            "Name one specific step in each category.",
        ),
        (
            "Potential roles or perspectives—not claims of consultation or approval:\n\n- ..." not in text,
            "Future review roles are identified",
            "Name relevant roles or perspectives without implying review, permission, or approval.",
        ),
        (
            "assets/hero/hero.png" not in text,
            "Default hero image is replaced",
            "Replace the template hero with a public-safe, project-relevant image.",
        ),
        (
            "|  |  |  |  |" not in text,
            "People table has at least one entry",
            "Add one short row per teammate; do not publish private contact details.",
        ),
        (
            "- **Code/notebooks:** ..." not in text
            and "- **Data and terms:** ..." not in text
            and "- **Reuse notes:** ..." not in text,
            "Reuse and provenance notes are complete",
            "Add stable links, source terms, citations, and concise reproduction notes.",
        ),
    ]


def write_report(issues: list[str], checks: list[tuple[bool, str, str]]) -> None:
    lines = ["# Site Health", ""]
    if not issues:
        lines.append("✓ No structural, navigation, or link issues detected.")
    else:
        lines.extend(["## Structural checks", ""])
        lines.extend(issues)
    lines.extend(["", "## Completion coach", ""])
    for complete, label, guidance in checks:
        if complete:
            lines.append(f"- ✓ **{label}**")
        else:
            lines.append(f"- ⚠ **{label}:** {guidance}")
    lines.extend([
        "",
        "This report is generated automatically during the site build. Warnings do not block publishing.",
        "",
        "The completion coach is an editing aid. It does not validate scientific claims, ethics, sovereignty, community fit, consultation, permission, approval, or authority.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    issues = (
        missing_file_issues()
        + missing_asset_dir_issues()
        + placeholder_issues()
        + navigation_issues()
        + schedule_issues()
        + internal_link_issues()
        + sticker_validation_issues()
        + people_gallery_issues()
    )
    checks = completion_checks()
    incomplete = sum(not complete for complete, _, _ in checks)
    write_report(issues, checks)
    print(
        f"Generated {REPORT.relative_to(ROOT)} with {len(issues)} structural warning(s) "
        f"and {incomplete} incomplete Home item(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
