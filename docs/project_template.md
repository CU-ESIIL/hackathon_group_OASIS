---
layout: default
title: "OASIS: 1.5-Day Hackathon Template"
subtitle: "A friction-free guide for collaborative research sprints"
hero_image: assets/template/hero.svg
team_logo: assets/template/team-logo.svg
contact_slack: "#oasis-project-room"
contact_email: "team@example.org"
repo_owner: "cu-esiil"
repo_name: "hackathon_group_OASIS"
edit_path: "docs/project_template.md"
---

# {{ page.title }}

{{ page.subtitle }}

{% if page.hero_image %}
<img src="{{ page.hero_image }}" alt="Hero Image" />
{% else %}
<div style="width:100%;height:200px;background:#eee;display:flex;align-items:center;justify-content:center;">Set `hero_image` in front matter</div>
{% endif %}

{% if page.team_logo %}
<img src="{{ page.team_logo }}" alt="Team Logo" />
{% endif %}

[📣 Edit this page](https://github.com/{{ page.repo_owner }}/{{ page.repo_name }}/edit/main/{{ page.edit_path }})

Slack: {{ page.contact_slack }} · Email: [{{ page.contact_email }}](mailto:{{ page.contact_email }})

*If this link 404s, set `repo_owner`, `repo_name`, and `edit_path` in the front matter.*

<nav style="position:sticky; top:0; background:#fff; padding:0.5rem; border-bottom:1px solid #ccc;">
[Day 1](#day1) · [Day 2](#day2) · [Resources](#resources)
</nav>

## Contents
- [Day 1](#day1)
- [Day 2](#day2)
- [Resources](#resources)
- [FAQ](#faq)

<a id="day1"></a>
<details>
<summary><strong>Day 1 — Align, Set Up &amp; Build</strong></summary>

### Objectives
- Form your team and assign roles
- Draft a project one-liner to align expectations
- Swap in your hero and team images
- Make and push your first commit
- Choose one primary output and build a useful first version

### Steps
1. **Project One-liner** – In one sentence, describe what you will explore.  
   *Example: *Collect and analyze rainfall data to model flash flood risks.*
2. **Edit this page** – Replace placeholders in the front matter above.
3. **Team Roles** – Fill in the table:

```markdown
| Role  | Name | Responsibilities |
|---|---|---|
| Lead | _(your name)_ | Coordinates tasks, keeps time |
| Data | _(your name)_ | Finds/preps data, documents sources |
| Methods | _(your name)_ | Runs analysis, records parameters |
| Comms | _(your name)_ | Summarizes outcomes, crafts visuals |
```

4. **Choose one output** – Focus on one figure, map, prototype, workflow, brief, decision framework, notebook, or next-step plan.
5. **Build and document** – Record data sources, methods, evidence, obstacles, and an early artifact as you work.
6. **Swap Images** – Follow the Image Replacement Micro-Guide in [Resources](#resources) to update `hero_image` and insert a team photo.
7. **Commit & Push**
   - *Web editor:* click **✏️ Edit this page**, make changes, write a short commit message, and **Commit changes**.  
   - *Clone route:* `git clone <repo-url>` → edit locally → `git add -A` → `git commit -m "initial setup"` → `git push`.

### Copy-paste Snippet
```markdown
Project one-liner: _(write it here)_
```

### Day 1 Checklist
- [ ] One-liner added
- [ ] Team roles filled
- [ ] Hero & team images swapped
- [ ] One focused output has a useful first version
- [ ] Evidence, methods, or a clear obstacle is documented
- [ ] Commit pushed to main

</details>

<a id="day2"></a>
<details>
<summary><strong>Day 2 — Finish, Validate &amp; Share</strong></summary>

### Objectives
- Finish and validate the most useful artifact
- State one or two evidence-backed claims
- Name confidence, limitations, and next steps
- Prepare one cumulative Hackathon Report Out

### Steps
1. **Reconfirm the finish line** – Decide what must work, what needs checking, and what can be dropped.
2. **Explore Libraries** – Start with these resources:
   - [Data Library](https://example.com/data-library) – replace with real link.
   - [Analytics Library](https://example.com/analytics-library) – replace with real link.
3. **Select Data** – Choose one dataset and note its source.
   *Example: *NOAA daily precipitation for Boulder County.*
4. **Set Up Tools** – Optional `gocmd` quickstart for Linux:

```bash
# Linux quickstart
GOCMD_VER=$(curl -L -s https://raw.githubusercontent.com/cyverse/gocommands/main/VERSION.txt); \
curl -L -s https://github.com/cyverse/gocommands/releases/download/${GOCMD_VER}/gocmd-${GOCMD_VER}-linux-amd64.tar.gz | tar zxvf -
./gocmd init

# Quick sanity check: can you list your home?
./gocmd ls i:/iplant/home/YOUR_USER
```

   > *(macOS uses a different tarball)*
5. **Minimal Analysis** – Run one of the snippets:

```python
# Python example
import pandas as pd
url = "https://example.com/data.csv"  # replace with real URL
df = pd.read_csv(url)
print(df.head())
```

```r
# R example
url <- "https://example.com/data.csv"  # replace with real URL
df <- read.csv(url)
head(df)
```

6. **Record Results** – Save a figure into `assets/results/`:

```markdown
<!-- Save figures into assets/results/ and reference below -->
![Result Figure](assets/results/example.png)
```

7. **Document Learnings** – State what the evidence supports, confidence, the main limitation, and what another group can reuse.
8. **Prepare the report-out** – Use the Home page to walk through why, question, artifact, evidence, confidence, limitations, reuse, and next steps.

### Day 2 Checklist
- [ ] Dataset chosen and cited
- [ ] Analysis snippet executed
- [ ] Figure saved to assets/results/
- [ ] Notes captured in Results section
- [ ] One or two claims include evidence and confidence
- [ ] Limitations and reusable outputs are listed
- [ ] Final report-out is ready

</details>

## Resources
<a id="resources"></a>

### Image Replacement Micro-Guide
1. **Save** your image as a simple filename, e.g., `team.jpg` (no spaces).
2. **Upload** it to `docs/assets/team/` (or `assets/team/` if this page is at repo root).
3. **Reference** it in Markdown: `![Team Photo](assets/team/team.jpg)`.
4. If the image doesn’t show: check for typos and confirm the path in GitHub.

```markdown
<!-- Replace the image below with your team photo -->
![Team Photo](assets/team/team.jpg)
```

*Encourage per-team folders like `assets/team-alpha/`, `assets/team-bravo/`, etc., to avoid collisions.*

> **Tip:** If your image doesn’t render, open it in the repo to copy the exact path.
> **Warning:** Don’t rename folders in `assets/` after linking them on the page.

### Common Pitfalls & How to Avoid Them
- [ ] Broken image paths → use `assets/<team>/filename.ext` and avoid spaces.
- [ ] Editing the wrong file → use the **Edit this page** link; confirm `edit_path`.
- [ ] Merge conflicts → if collaborating, prefer **web edits** + short, frequent commits.
- [ ] Pushing from cloud notebooks → verify SSH is configured or use the web editor.

## FAQ
<a id="faq"></a>

**Q: The edit link doesn’t work.**  
A: Update `repo_owner`, `repo_name`, and `edit_path` in the front matter.

**Q: Where do I put large data files?**  
A: Store them outside the repo and link to them in `docs/data.md`.

**Q: Can I use branches?**  
A: Yes, but for quick sprints stick to `main` and small commits.

---

<small>
{{ page.repo_name }} — Last updated {{ site.time | date: "%Y-%m-%d" }} · Slack: {{ page.contact_slack }} · Email: [{{ page.contact_email }}](mailto:{{ page.contact_email }})
</small>
