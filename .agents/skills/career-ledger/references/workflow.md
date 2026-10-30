# Career Ledger Workflow

## Classify and route

Follow a clear request directly. Otherwise route from `make inspect`:

- `missing` or `empty`: ask whether to (1) import a CV/resume or (2) use a guided interview.
- `invalid`: run `make validate` and repair structural errors before intake.
- `populated`: run `make validate`; if scope is unclear, ask whether to (1) update the profile or (2) generate a resume. Route resume requests to `resume-router`.

For a populated profile, briefly summarize its coverage and unresolved notes before continuing.

Reconcile imports against existing facts. Do not duplicate matches, persist source documents, copy promotional prose, or upgrade unsupported claims.

## Structure the database

Keep schema-required root keys; `education`, `employment`, and `projects` may be empty. Sort known employment dates newest first. Store projects only at root; link them through unique IDs in optional `employmentId`. Project weights are independent integers from 1–10.

## Interview factual gaps

Ask the highest-value unanswered question, then recompute. Do not ask for known facts or suggest biographical answers. For projects, probe situation, task, action, result, skills, and relevance; STAR fields are limited to 100 characters.

Close answers marked unknown, approximate, private, skipped, out of scope, or finished. Record only material unresolved gaps in top-level `notes`.

## Classify and preserve facts

- Keep approximations approximate and prefer qualitative results to invented metrics.
- Exclude confidential or employer-sensitive material.
- Match by stable ID first, then organization, role, subject, and dates.
- Reuse skill IDs while keeping each project's name, keywords, and proficiency local.
- Exclude `private: true` records from application materials.

## Write safely

After each confirmed answer, re-read the target, build a targeted candidate, validate it, reconcile concurrent changes, then patch. Never write an invalid candidate.

Run `make check` when scope is complete. Report changed records, approximations, private records, unresolved notes, and validation results.
