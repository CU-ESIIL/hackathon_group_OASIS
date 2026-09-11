# OLC Climate Resiliency Hackathon · OASIS Template

We're watching ty edit. 
This repository is the OASIS team-workspace template for the OLC Climate Resiliency and Digital Sovereignty Hackathon on September 15–16, 2026. It adapts the [source OLC curriculum](https://github.com/olc-techsupport/Education-Climate-Resiliency-Digital-Sovereignty) while preserving the reusable OASIS instructions, public-page, and report-out views.

The website is built from the docs/ folder using MkDocs.

## Preview locally

pip install -r requirements.txt
mkdocs serve

## Build site

mkdocs build --strict --clean

## Site Health

The site generates a non-blocking health report during the build.

The generated `docs/_site_health.md` report flags structural problems and coaches teams through common incomplete fields.

Warnings do not prevent the site from publishing, and the completion coach does not validate scientific claims, ethics, sovereignty, community fit, review, or approval.

## Editing Pages

Use the edit icon on the website to open the corresponding markdown file in GitHub edit mode.

## Team Profiles

Each person has their own Markdown profile file in `docs/people/`. The homepage People gallery reads those files at build time. Use `docs/_data/people.yml` only as an index of profile paths, for example `profile: people/your-name.md`; do not duplicate profile text in YAML.

## Citations

Add BibTeX entries to `docs/references.bib`, then cite them in Markdown with `[@citationKey]`. The site build renders the References section automatically.

## Completing the Project Story

Use the Home page as a synthesis checklist, not an activity log: Question → Evidence → Representation → Build → Interpret → Uncertainty → Stewardship → Share. Add specific observations, link them to a figure, notebook, PDF, dashboard, data product, or another artifact, and state the evidence boundary plainly.

Strong entries state what happened, why it matters, what evidence supports it, what remains uncertain, who should help with a continuation, and what another group can reuse. Keep the report-out sections short enough for a 5–6 minute walkthrough unless facilitators set another allotment.

## GitHub Pages

This site is automatically built and deployed using GitHub Actions.

## License

This template is released under the MIT License.
