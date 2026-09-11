from __future__ import annotations

from pathlib import Path

from check_stickers import sticker_issues


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    errors: list[str] = []
    index = read("docs/index.md")
    olc_example = read("docs/olc-example.md")
    fire_example = read("docs/example.md")
    directions = read("docs/instructions.md")
    day1 = read("docs/instructions/day1.md")
    day2 = read("docs/instructions/day2.md")
    day3 = read("docs/instructions/day3.md")
    stewardship = read("docs/instructions/stewardship.md")
    cubedynamics = read("docs/instructions/cubedynamics.md")
    facilitator = read("docs/facilitator-guide.md")
    project_template = read("docs/project_template.md")
    mkdocs = read("mkdocs.yml")
    css = read("docs/stylesheets/extra.css")
    mode_toggle = read("docs/javascripts/mode-toggle.js")
    presentation = read("docs/javascripts/presentation-mode.js")
    health = read("scripts/site_health.py")

    require(bool(index), "docs/index.md is missing.", errors)
    require("public_mode_toggle: true" in index, "Home should keep the instructions toggle marker.", errors)
    require("September 15–16, 2026" in index, "Home should name the event dates.", errors)
    require("Question → Evidence → Representation → Build → Interpret → Uncertainty → Stewardship → Share" in index,
            "Home should show the participant journey.", errors)
    require("[See the completed OLC example](olc-example.md)" in index,
            "Home should link to the completed OLC example.", errors)
    require("[See the completed fire example](example.md)" in index,
            "Home should retain a link to the fire example.", errors)
    require("| Name | Affiliation | Contact | Starting role |" in index and "|  |  |  |  |" in index,
            "Home should retain an empty editable People table.", errors)
    require(index.count(".oasis-report-out-section") == 6,
            "Home should expose exactly six report-out story sections.", errors)
    for section in [
        "## Our Question 📣",
        "## Why This Matters 📣",
        "## What We Tried to Build 📣",
        "## Data and Evidence",
        "## Methods and Tools",
        "## What We Made",
        "## What We Learned 📣",
        "## What Didn’t Work",
        "## What Remains Uncertain 📣",
        "## What’s Next 📣",
        "## Who Should Be Involved Next",
        "## Code, Data, Citation and Reuse",
    ]:
        require(section in index, f"Home section missing: {section}.", errors)
    require(index.count("Sovereignty checkpoint") == 3,
            "Home should retain all three sovereignty checkpoints.", errors)
    require("Accessible ≠ interpretable ≠ actionable" in index,
            "Home should state the public-data evidence boundary.", errors)
    require("{{ references }}" in index and "[@oasisProjectTemplate]" in index,
            "Home should keep the BibTeX citation flow.", errors)
    require("<div" not in index and "<table" not in index,
            "Home should stay Markdown-first without raw layout HTML.", errors)

    require("# When Drought Reaches the River" in olc_example,
            "The completed OLC example should remain available.", errors)
    require("Spearman ρ = 0.56" in olc_example and "Does this tell us whether livestock had enough water? No." in olc_example,
            "The OLC example should retain its result and explicit evidence boundary.", errors)
    require("olc_drought_streamflow_example.py" in olc_example and "analysis_metrics.json" in olc_example,
            "The OLC example should link its reproducible outputs.", errors)
    require("{{ references }}" in olc_example and "[@olcClimateResiliency]" in olc_example,
            "The OLC example should preserve source attribution.", errors)

    require("# How Fast is a Fire?" in fire_example, "The completed fire example should remain intact.", errors)
    require("{{ references }}" in fire_example and "[@oasisProjectTemplate]" in fire_example,
            "The fire example should demonstrate the citation flow.", errors)

    require("# OLC Climate Resiliency Hackathon Directions" in directions,
            "Directions should identify the OLC Hackathon.", errors)
    require("instructions/day1.md" in directions and "instructions/day2.md" in directions,
            "Directions should link both active day guides.", errors)
    require("instructions/stewardship.md" in directions and "instructions/cubedynamics.md" in directions,
            "Directions should link stewardship and optional CubeDynamics guidance.", errors)
    require("instructions/day3.md" not in directions,
            "Directions should not present Day 3 as an active guide.", errors)
    require("September 15, 2026" in day1 and "4:15–4:45" in day1,
            "Day 1 should include the source-curriculum date and peer-review window.", errors)
    require("September 16, 2026" in day2 and "10:45–11:45" in day2,
            "Day 2 should include the source-curriculum date and sharing window.", errors)
    require("5–6 minutes" in day2 and "Hackathon Report Out" in day2,
            "Day 2 should explain the OASIS report-out.", errors)
    require("older bookmarks" in day3 and "1.5-day Hackathon" in day3,
            "The legacy Day 3 route should redirect readers to the active workflow.", errors)
    require("Accessible ≠ interpretable ≠ actionable" in stewardship and "does not establish sovereignty compliance" in stewardship,
            "Stewardship guidance should state its boundary and non-certification disclaimer.", errors)
    require("no public PyPI package or GitHub Release" in cubedynamics and "checksum-verified" in cubedynamics,
            "CubeDynamics guidance should retain its current prerelease safety boundary.", errors)
    require("Fast novice check" in facilitator and "reviewers ask questions; they do not certify" in facilitator.lower(),
            "The facilitator guide should include novice and non-certification checks.", errors)

    require("1.5-Day Hackathon Template" in project_template,
            "The alternate template should use the current event length.", errors)
    require("#day3" not in project_template and "Day 3 Checklist" not in project_template,
            "The alternate template should not expose an active Day 3 workflow.", errors)

    require("  - OLC Example: olc-example.md" in mkdocs and "  - Fire Example: example.md" in mkdocs,
            "MkDocs navigation should expose both examples.", errors)
    require("  - Directions:" in mkdocs and "  - Facilitator Guide: facilitator-guide.md" in mkdocs,
            "MkDocs navigation should expose directions and facilitator guidance.", errors)
    require("CU-ESIIL/hackathon_group_OASIS" in mkdocs and "Project_group_OASIS" not in mkdocs,
            "MkDocs metadata should use the current repository identity.", errors)
    require("  - Summit Team Sites:" not in mkdocs and "  - Summit Team Sites Gallery:" not in mkdocs,
            "Legacy Summit galleries should not appear in active navigation.", errors)

    require("template-guidance-toggle" in mode_toggle and "Instructions on" in mode_toggle,
            "Instructions on/off behavior is missing.", errors)
    require("isHomePage" in presentation and "h2.oasis-report-out-section" in presentation,
            "Presentation mode should remain scoped to marked project-story sections.", errors)
    require('h2#people' not in presentation,
            "Presentation mode should not add unmarked People content to the six-section story.", errors)
    require("Hackathon Report Out" in presentation,
            "Presentation controls should use Hackathon Report Out terminology.", errors)
    require("oasis-report-out-section-visible" in presentation and "oasis-report-out-section-visible" in css,
            "Presentation mode should use the cumulative section class.", errors)
    require("body.presentation-mode .md-typeset > *" in css,
            "Presentation mode should continue hiding non-report-out content.", errors)

    require("def completion_checks" in health and "The completion coach is an editing aid" in health,
            "Site health should retain the non-blocking completion coach and disclaimer.", errors)

    stale = "Project_group_OASIS"
    for relative_path in ["docs/index.md", "docs/olc-example.md", "docs/example.md", "docs/instructions.md", "mkdocs.yml"]:
        require(stale not in read(relative_path), f"Stale repository identity remains in {relative_path}.", errors)

    sticker_errors = sticker_issues()
    require(not sticker_errors, "Retired sticker cleanup failed:\n" + "\n".join(sticker_errors), errors)

    if errors:
        print("Template regression check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Template regression check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
