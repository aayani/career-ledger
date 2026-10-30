---
name: career-ledger
description: Create, update, reconcile, or audit the canonical career evidence database through guided interviews or source-document intake. Use for career timelines, career-history intake, evidence clarification, CV import as source material, or maintaining career.yaml. Do not use to generate resumes, CVs, or cover letters as deliverables.
user-invocable: false
disable-model-invocation: false
---

# Career Ledger

Maintain `career.yaml` as a neutral, evidence-aware source of truth. A supplied CV is evidence input, not a resume deliverable; do not invoke `resume-cover-letter`.

## Route the session

From the repository root, read [workflow.md](references/workflow.md), inspect `career.yaml`, and follow only the applicable route.

Before creating the database or changing its structure, read [schema.yaml](references/schema.yaml) and inspect `tests/fixtures/career-valid.yaml`. The JSON Schema expressed in YAML is authoritative. The scripts load and enforce it directly.

## Invariants

- Treat the repository's `scripts/` directory as read-only during career-ledger data work. Existing scripts may be inspected or executed, but never create, edit, delete, rename, move, or format files under `scripts/`.
- Never invent or strengthen career facts.
- During guided intake, ask exactly one question per turn. Never bundle multiple questions into one sentence, list, or prompt.
- Preserve stable employment and skill IDs, unrelated records, and concurrent user changes according to the workflow.
- Model skills as groups: `name` identifies the capability area and `keywords` lists its tools, frameworks, methods, and technologies.
- A repeated skill ID may carry different names, keywords, or proficiency values across project usages as the skill evolves.
- Use `private: true` only for education, employment, or skill usages that must not be disclosed.
- Store material unresolved gaps as concise top-level `notes`, not speculation or hidden session state.
- Stop immediately when the user pauses or finishes. Save only confirmed work and report validation honestly.
