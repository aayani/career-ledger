---
name: career-timeline
description: Create, update, reconcile, or audit the canonical career evidence database through guided interviews or source-document intake. Use for career timelines, career-history intake, evidence clarification, CV import as source material, or maintaining docs/career.md. Do not use to generate resumes, CVs, or cover letters as deliverables.
---

# Career Timeline

Maintain `docs/career.md` as a neutral, evidence-aware source of truth. A supplied CV is evidence input, not a resume deliverable; do not invoke `resume-cover-letter`.

## Route the session

From the repository root, read [workflow.md](references/workflow.md), inspect `docs/career.md`, and follow only the applicable route.

Before creating the database or changing its structure, read [career-schema.yaml](references/career-schema.yaml) and inspect `tests/fixtures/career-valid.md`. The YAML file is authoritative for structure and authoring policy. The scripts load and enforce it.

## Invariants

- Treat the repository's `scripts/` directory as read-only during career-timeline work. Existing scripts may be inspected or executed, but never create, edit, delete, rename, move, or format files under `scripts/`.
- Never invent or strengthen career facts.
- During guided intake, ask exactly one question per turn. Never bundle multiple questions into one sentence, list, or prompt.
- Preserve stable IDs, unrelated records, disclosure restrictions, and concurrent user changes according to the workflow.
- Store material unresolved gaps as follow-ups, not speculation or hidden session state.
- Stop immediately when the user pauses or finishes. Save only confirmed work and report validation honestly.
