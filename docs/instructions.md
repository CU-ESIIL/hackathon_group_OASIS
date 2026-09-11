---
title: Hackathon Directions
---

# OLC Climate Resiliency Hackathon Directions

These pages translate the [OLC Climate Resiliency and Digital Sovereignty Learning Lab curriculum](https://github.com/olc-techsupport/Education-Climate-Resiliency-Digital-Sovereignty) into a focused OASIS workflow for **September 15–16, 2026** [@olcClimateResiliency]. The source curriculum remains authoritative for the event schedule, teaching materials, prepared public datasets, and pathway notebooks.

- **Day 1 — September 15:** [Question, Evidence, and Build](instructions/day1.md)
- **Day 2 — September 16:** [Interpret, Steward, and Share](instructions/day2.md)
- **Throughout:** [Public Data and Stewardship](instructions/stewardship.md)
- **Optional:** [Want to Go Further with CubeDynamics?](instructions/cubedynamics.md)

[Edit your team page](https://github.com/CU-ESIIL/hackathon_group_OASIS/edit/main/docs/index.md){ .md-button .md-button--primary target="_blank" rel="noopener" }
[Open the completed OLC example](olc-example.md){ .md-button }

## Your 1.5-day journey

**Question → Evidence → Representation → Build → Interpret → Uncertainty → Stewardship → Share**

| Stage | Ask | Leave behind |
|---|---|---|
| Question | What can we investigate responsibly in the available time? | One focused question and a definition of progress |
| Evidence | What do the public data measure, where, when, and for whom? | Source, place, period, meaning, and limitations |
| Representation | What is included, transformed, averaged, or missing? | A defensible analytical or design choice |
| Build | What is the smallest useful thing we can make? | One visible artifact or documented attempt |
| Interpret | What happened, and what do we think it means? | Observation, evidence, and interpretation |
| Uncertainty | What can we not claim? | A precise evidence boundary |
| Stewardship | Who should help frame, interpret, or review a continuation? | Named roles and unresolved needs, without implied approval |
| Share | What can another person understand and reuse? | A public-safe page and short report-out |

## Three pathways, one standard of care

Choose the support pathway that fits the team’s question and working style. These are parallel approaches, not prestige levels.

- **Guided Explorer:** inspect, visualize, and explain what the evidence shows and does not show.
- **Data Investigator:** compare datasets, coverage, transformations, assumptions, or sensitivity.
- **Technical Extender:** test, reproduce, or extend a method while documenting enough for someone else to rerun it.

Teams can combine pathways or switch when the evidence changes the question. A clear figure or documented limitation can be more useful than a complicated but uninterpretable model.

## Minimum success

By noon on September 16, every team should have:

- One focused question
- One visible artifact, early result, or well-documented attempt
- One evidence-backed learning
- One honest uncertainty or failed approach
- One responsible next step
- A page containing only material appropriate for public sharing

## Seven-question coverage check

The full project page should let a new reader answer all seven questions, even though they do not need seven separate sections:

1. What question did you explore, and why?
2. What did you learn?
3. What did you create or try to create?
4. What remains uncertain?
5. What would you investigate next?
6. Who might benefit if this work eventually succeeds?
7. Who should review or help interpret a continuation?

The short report-out compresses these answers into the six megaphone sections.

## One page, three views

The Home page serves three purposes without asking participants to maintain slides separately:

- **Instructions on:** prompts and examples appear while the team works.
- **Instructions off:** the same Markdown becomes a cleaner public project page.
- **Hackathon Report Out:** only the marked story sections appear for the final walkthrough.

The report-out should move through the question, importance, intended build, learning, uncertainty, and next step. Aim for **5–6 minutes** unless facilitators set a different allotment based on the number of teams.

## Public-data boundary

The Hackathon works with prepared public environmental datasets. Public availability makes short-event analysis possible; it does not establish that the evidence is locally sufficient, culturally complete, appropriate for every use, or ready to guide a real decision.

**Accessible ≠ interpretable ≠ actionable.** Read [Public Data and Stewardship](instructions/stewardship.md) before publishing interpretations.

## Editing workflow

Most participants only need to edit `docs/index.md`, upload artifacts under `docs/assets/`, and add BibTeX records to `docs/references.bib`.

1. Use an **Edit** button on Home or edit `docs/index.md` in GitHub.
2. Replace `...` and default artifacts as the work develops.
3. Add source links, captions, and evidence boundaries while they are fresh.
4. Commit small changes often and refresh the published site.
5. Preview with **Instructions off** and **Hackathon Report Out**.
6. Review the non-blocking [site completion coach](_site_health.md).

The coach finds common blank-template and link issues. It does not validate science, ethics, sovereignty, community fit, consultation, or approval.

## Where files go

| Location | Use |
|---|---|
| `docs/index.md` | Editable team page and report-out |
| `docs/olc-example.md` | Completed, annotated OLC public-data example |
| `docs/example.md` | Preserved advanced fire-analysis example |
| `docs/assets/hero/` | Public-safe banner image |
| `docs/assets/whiteboards/` | Working notes and sketches |
| `docs/assets/explorations/` | Early plots, screenshots, and rough maps |
| `docs/assets/figures/` | Main figures and final visuals |
| `docs/assets/files/` | Briefs and other downloads |
| `code/` | Scripts, notebooks, and reproducible workflows |
| `docs/references.bib` | BibTeX records used by `[@citationKey]` references |

Large or restricted data do not belong in the public repository. Follow facilitator-provided storage instructions and the data steward’s terms.

{{ references }}
