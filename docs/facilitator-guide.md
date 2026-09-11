---
title: Facilitator Guide
---

# Facilitator Guide

This is a short run-of-show for the **OLC Climate Resiliency and Digital Sovereignty Hackathon, September 15–16, 2026**. Use the [source OLC curriculum](https://github.com/olc-techsupport/Education-Climate-Resiliency-Digital-Sovereignty/tree/main/2026%20Buildathon) for authoritative teaching materials and schedule details.

## The outcome to protect

Every team leaves with one focused question, one visible artifact or documented attempt, one evidence-backed learning, one honest uncertainty, one responsible next step, and a public-safe OASIS page. Do not make technical complexity the implicit measure of success.

## Day 1 prompts

| Time | Facilitation move |
|---|---|
| 9:30–10:30 | Introduce the three parallel pathways. Form teams and press for one scoped question. Ask checkpoint 1: who framed it, and do the public data fit? |
| 10:45–noon | Require source, place, period, units, meaning, and coverage before analysis expands. By lunch, each team should have a question and one evidence-table row. |
| Noon | Present CubeDynamics as optional. Use it only if the verified facilitator-provided environment is ready. |
| 1:00–3:00 | Ask for the smallest useful artifact. Encourage teams to save a working visual early and document decisions in OASIS. |
| 3:15–4:15 | Press for an observation tied directly to evidence. Normalize null results, failed attempts, and revised questions. |
| 4:15–4:45 | Pair teams for evidence and stewardship review. Reviewers ask questions; they do not certify the work. |
| 4:45–5:00 | Confirm persistent saves and require one named first task for Day 2. |

## Day 2 prompts

| Time | Facilitation move |
|---|---|
| 9:00–10:00 | Protect the finish window. Discourage new directions; ask what needs validation and what can be dropped. |
| 10:15–10:45 | Have teams complete observation, evidence, interpretation, uncertainty, stewardship, and next step. Preview Instructions off and Report Out. |
| 10:45–11:45 | Share from OASIS. Aim for 5–6 minutes per team unless team count requires another allotment. |
| 11:45–noon | Reflect on what the public data enabled, what they could not establish, and what responsible continuation would require. |

## Pathway coaching

- **Guided Explorer:** ask for a clear explanation of one pattern and one non-claim.
- **Data Investigator:** ask which coverage or analytical choice changes interpretation.
- **Technical Extender:** ask whether another person can reproduce the method and whether added complexity improves the science.

Pathways are not ranked. Teams may combine or switch them.

## Questions to use while circulating

- **Question:** Can your data actually help answer that?
- **Data:** What does one value, row, pixel, or observation physically represent?
- **Build:** What is the smallest useful thing you could finish today?
- **Interpretation:** Show me the evidence for that sentence.
- **Representation:** Who or what is not represented by this dataset?
- **Uncertainty:** What could you not conclude?
- **Stewardship:** Who should be involved before this interpretation travels farther?
- **Synthesis:** If the code never works, what did you learn that another team could reuse?

## Public-data and sovereignty guardrails

Repeat: **Accessible ≠ interpretable ≠ actionable.** Public availability does not make evidence locally sufficient or authorize use. Keep culturally sensitive knowledge, protected locations, restricted data, personal information, and unapproved claims off public GitHub.

The three sovereignty checkpoints are reflection prompts, not certification. Do not describe a person, Tribe, community, office, OLC, or another organization as a reviewer, collaborator, authority, or endorser unless that relationship has actually occurred and can be stated publicly.

## Pre-event data provenance check

The OASIS example pins the source curriculum at commit `a1d5b5b`. At that commit, the manifest hashes for the original NOAA and USGS snapshots verify, and rerunning `prepare_teaching_data.py` produces these prepared-file hashes:

- `drought_monthly.csv`: `c2b400a135daa36631bf35ae0dd0f422b72d8a71d11a023312aff9cbc92dbd00`
- `streamflow_daily.csv`: `73a24f5dc5d74173fc4857d42aa68b541e2d7694be9d5a51b50c842af2ffab4c`

The committed `teaching_checksums.json` in that source revision lists different prepared-file hashes. Treat this as an upstream provenance inconsistency for human review: reconcile or regenerate that checksum file before asking participants to use it as a verification target. The OASIS example script verifies the reproduced hashes above and records them in its output metadata.

## Fast novice check

Ask one person who did not edit the page to find, without coaching:

1. The team question
2. What one data value represents
3. The main artifact
4. The evidence-backed learning
5. The largest uncertainty
6. The next technical and stewardship steps

If any item takes more than a minute, simplify the heading, opening sentence, caption, or link. The [site completion coach](_site_health.md) can flag common omissions, but it cannot judge scientific validity, community fit, sovereignty, ethics, or approval.
