# Career Ledger Workflow

## Classify and route

Run `make inspect`, then use these states:

- `missing` or `empty`: explain that the database stores neutral career facts, then present exactly these two onboarding options and wait for the user's choice:
  1. **Import from CV/resume:** use an existing document as source material.
  2. **Guided interactive interview:** build the career record one question at a time.
- `invalid`: run `make validate` and repair structural errors before intake.
- `populated`: run `make validate` before making unrelated updates.

For a valid populated database, orient the user with its current location, latest employment, covered education and employment records, project count, skill-usage count, private-record count, and unresolved top-level notes. Follow the requested scope instead of presenting another menu.

Treat imported claims as matching, new, richer, conflicting, or ambiguous. Do not duplicate or re-ask matching claims. A source CV is evidence input: do not persist it, copy promotional prose, or treat it as stronger than the source supports.

## Structure the database

Keep the root keys required by the schema. Empty `education`, `employment`, and `projects` arrays are valid. Keep employment in reverse chronological order when dates are known. Store projects only in the root `projects` array. Link a project to one or more jobs with its optional `employmentId` array; every ID must match an existing employment record. Omit the field for independent work. Keep project relevance weights independent; they are integer scores from 1 to 10 and do not need to total 10.

## Interview factual gaps

Build a dependency tree for the selected scope and ask the single frontier question that unlocks the most useful next branch. Recompute after each answer. Inspect the repository and supplied sources before asking for facts already available.

Do not suggest biographical answers such as employers, dates, results, skills, or source details. Useful project probes cover the situation, task, action, result, relevant skills, and relative relevance. Keep each STAR field concise and within 100 characters.

Close a branch when answered or when the user marks it unknown, approximate, private, skipped, out of scope, paused, or finished. Do not pressure the user to reopen it in the same session. Add a top-level note only when the unresolved gap would materially improve a future application.

## Classify and preserve facts

- Never turn an approximate fact into an exact one.
- Exclude confidential documents, credentials, internal URLs, customer data, and employer-sensitive material from project narratives.
- Prefer accurate qualitative results over invented metrics.
- Keep `private: true` records out of application materials.
- Reuse a stable skill-group ID across project usages while keeping the usage's group name, keywords, and optional proficiency local to that project.
- Preserve employment IDs through wording and factual corrections.
- Match records by stable ID first, then organization, role, subject, and dates.

Make targeted edits, retain unrelated content and privacy flags, and reconcile concurrent changes before writing.

## Write safely

1. Re-read `career.yaml` and retain its baseline.
2. Build a complete candidate outside the target.
3. Run `make validate path=<candidate>`.
4. Do not replace the target while errors remain.
5. Re-read and reconcile any concurrent target change.
6. Apply the candidate through a patch or safe atomic replacement.
7. Run `make check` on the final repository.

Use `make validate-complete` only when a downstream resume workflow requires at least one employment and one skill usage. Report changed records, approximate values, private records, unresolved notes, and validation results.
