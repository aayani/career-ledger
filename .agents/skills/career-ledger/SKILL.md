---
name: career-ledger
description: Maintain data/profile.yaml from CV evidence, guided interviews, or targeted updates. Use for creating, reconciling, or auditing career facts; not resume or cover-letter deliverables.
user-invocable: true
disable-model-invocation: false
---

# Career Ledger

Maintain `data/profile.yaml` as the neutral source of truth. Accept CV/resume evidence, guided interviews, or targeted updates.

Read [workflow.md](references/workflow.md), then run `make inspect`. Before creating or restructuring the profile, read the authoritative [schema.yaml](references/schema.yaml) and `tests/fixtures/profile-valid.yaml`.

## Invariants

- Treat `scripts/` as read-only during profile work.
- Never invent or strengthen career facts.
- Ask one factual question per turn, save each confirmed answer promptly, and stop when the user pauses.
- Preserve stable IDs, unrelated records, privacy flags, and concurrent edits.
- Model skills as groups: `name` is the capability; `keywords` are its tools, frameworks, methods, and technologies.
- A repeated skill ID may carry different names, keywords, or proficiency values across project usages as the skill evolves.
- Use `private: true` only for undisclosable education, employment, or skill usages.
- Store material unresolved gaps as concise top-level `notes`; report validation honestly.
