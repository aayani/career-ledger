# Career Ledger Run Checklist

## Start

- [ ] Resolve the request to `audit`, `clarify`, `generate`, `import`, or `update`; list those choices if the argument is unsupported.
- [ ] Treat any new skill, project, achievement, or proficiency claim as `clarify`; use `update` only to correct or extend an already-evidenced record.
- [ ] Run `make inspect`.
- [ ] For a missing or empty profile, ask whether to import existing evidence or begin a guided interview.
- [ ] For an invalid profile, run `make validate`; report errors in `audit`, otherwise repair structural errors before intake.
- [ ] For a populated profile, run `make validate` and summarize coverage and unresolved notes.
- [ ] If the scope remains unclear, ask whether to update the profile or generate a resume.
- [ ] Before creating or restructuring the profile, read `schema.yaml` and `tests/fixtures/profile-valid.yaml`.

## Audit

- [ ] Check validation errors, duplicates, contradictions, privacy issues, unsupported claims, and material gaps.
- [ ] Report findings without changing the profile.

## Clarify

- [ ] Identify the highest-value open factual gap without re-asking known or closed facts.
- [ ] Ask one factual question without suggesting an answer, then wait.
- [ ] Classify the answer as confirmed, unknown, approximate, private, skipped, out of scope, or finished.
- [ ] For a new skill, resolve one factual question per turn: where it was used, personal contribution, tools, frameworks, or methods used, result, relevance, and contextual proficiency.
- [ ] Do not infer tools, keywords, proficiency, outcomes, or evidence links from adjacent profile content.
- [ ] Before writing a new skill, link it to a confirmed project and require at least one user-confirmed tool, framework, or method as a keyword.
- [ ] For projects and new skill evidence, capture situation, task, personal action, result, skills, tools or methods, and relevance; keep each STAR field within 100 characters.
- [ ] Re-read the profile, build and validate the candidate change, reconcile concurrent edits, and patch the confirmed answer.
- [ ] Recompute the gaps; repeat this section for another question or stop when the user pauses or finishes.

## Generate

- [ ] Invoke `resume-router` with the available profile evidence.
- [ ] Return to `career-ledger` only for profile errors or missing material facts.
- [ ] Record the generated artifact, validation result, gaps, assumptions, and approximations.

## Import

- [ ] Inventory the supplied evidence and extract candidate facts without persisting source documents or promotional prose.
- [ ] Match existing facts by stable ID, then organization, role, subject, and dates; reuse IDs and avoid duplicates.
- [ ] Preserve approximations, privacy flags, and unrelated records; prefer qualitative results to invented metrics and exclude confidential material.
- [ ] Map facts to the schema without strengthening claims.
- [ ] Re-read the profile, build and validate the reconciled candidate, preserve concurrent edits, and patch only supported facts.

## Update

- [ ] Identify the exact records and fields in scope.
- [ ] Confirm the change introduces no new skill, project, achievement, proficiency, or unsupported keyword; otherwise select `clarify`.
- [ ] Ask one factual question only when required to correct or extend an already-evidenced record.
- [ ] Preserve stable IDs, approximations, privacy flags, unrelated records, and confidential material.
- [ ] Re-read the profile, build and validate the targeted candidate, preserve concurrent edits, and patch only the requested facts.

## Finish

- [ ] Verify every new skill has confirmed usage context, personal contribution, and at least one confirmed keyword; do not persist unsupported candidate fields.
- [ ] Run `make check` when profile changes are complete.
- [ ] Report changed records, approximations, private records, unresolved notes, and validation results.
