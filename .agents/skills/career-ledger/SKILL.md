---
name: career-ledger
description: Maintain data/profile.yaml from evidence, interviews, or targeted updates. Generate requests route to resume-router.
user-invocable: true
disable-model-invocation: false
argument-hint: "[audit|clarify|generate|import|update]"
---

# Career Ledger

Maintain `data/profile.yaml` as the neutral source of truth.

## Arguments

1. `audit`: report validation errors, duplicates, contradictions, privacy issues, unsupported claims, and gaps. Do not write unless asked.
2. `clarify`: validate and inspect the profile, summarize gaps, then ask one high-value factual question per turn.
3. `generate`: invoke `resume-router`; return here only for profile errors or missing material facts.
4. `import`: reconcile supplied career evidence without duplicates or stronger claims.
5. `update`: change targeted facts, asking only for required information.

With no argument, follow the requested profile task. For an unsupported argument, list the five accepted arguments and ask the user to choose.

## Run checklist

Use the current session's `checklist.md`, created from this [template](references/checklist.md). Keep it current until handoff or completion.

## Invariants

- Treat `scripts/` as read-only during profile work.
- Never invent or strengthen career facts.
- Ask one factual question per turn. Save confirmed answers promptly. Stop when the user pauses.
- Preserve stable IDs, unrelated records, privacy flags, and concurrent edits.
- Follow schema descriptions for data modeling and privacy semantics.
  - Use this order for gathering facts: name, location, contact, education, then the rest.
  - When gathering facts for employment or project, confirm with user if they have anything else to add before jumping to the next job or project.
- Report validation honestly.
