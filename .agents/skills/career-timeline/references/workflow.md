# Career Timeline Workflow

## Classify and route

Run `python3 scripts/inspect_state.py docs/career.md`, then use these states:

- `missing` or `empty`: explain that the database stores neutral evidence, then present exactly these two onboarding options and wait for the user's choice:
  1. **Import from CV/resume:** use an existing document as unverified source material.
  2. **Guided interactive interview:** build the career record one question at a time.
- `populated`: run `python3 scripts/validate_career.py docs/career.md`. Repair structural errors before unrelated intake; warnings may remain when they describe honest data gaps.

Continue when the schema version matches the template. Explain and confirm any older-schema migration; stop structural edits for a newer or missing schema version.

For a valid populated database, orient the user with its last review, latest role, covered sections, open follow-ups, estimates, and unverified claims. Follow the scope they requested instead of presenting another menu. Resume an earlier interview from open follow-ups.

Treat imported claims as matching, new, richer, conflicting, or ambiguous. Do not duplicate or re-ask matching claims; present conflicts neutrally for the user to resolve. A source CV is evidence input: do not persist it, copy promotional prose, or treat it alone as verification. Clarifying gaps after an import is part of source reconciliation, not a third onboarding option.

## Interview factual gaps

Build a dependency tree for the selected scope and ask the single frontier question that unlocks the most useful next branch. Recompute after each answer. Inspect repository and supplied sources before asking for facts already available.

Do not suggest biographical answers such as employers, dates, metrics, technologies, ownership, or evidence sources. Useful achievement probes cover the prior problem, personal contribution, others' ownership, observed change, measurement quality, safe provenance, and disclosure.

If a material term remains unfamiliar after inspecting available sources, pause that branch and offer one question containing the applicable choices:

1. confirm a clearly labeled plausible meaning, when one genuinely exists;
2. authorize internet research and then confirm the result in the user's context; or
3. explain the term directly.

Close a branch when answered or when the user marks it unknown, approximate, private, skipped, out of scope, paused, or finished. Do not pressure the user to reopen it in the same session. Record a follow-up only when resolving the gap would materially improve an application.

## Classify and preserve facts

- `Verified`: confirmed by the user with honest provenance; described personal recollection is acceptable.
- `Estimated`: the event is confirmed but a date, quantity, scale, or result is approximate.
- `Unverified`: imported, inferred, conflicting, or insufficiently confirmed.

Evidence notes may cite safe provenance but never store source documents, credentials, internal URLs, customer data, proprietary details, or employer-sensitive material. Prefer accurate qualitative outcomes over invented metrics.

Choose ownership from demonstrated contribution: `Lead`, `Primary`, `Shared`, `Contributor`, or `Support`. Add `Disclosure: Interview-only` or `Disclosure: Do not disclose` only as exceptions to the application-safe default.

Match records by stable ID, then type, organization, subject, and dates. Preserve IDs through wording and factual corrections. Make targeted edits, retain unrelated content and disclosure restrictions, keep employers reverse chronological, and maintain typed references.

The user's requested update and clarified answers authorize a coherent write once facts, provenance, verification, ownership, disclosure, conflicts, and uncertainty are resolved. Ask for confirmation only when a material choice remains, a value would be inferred, sources conflict, an unresolved claim would be preserved, or migration would reinterpret records.

## Write safely

1. Re-read the target and retain its baseline.
2. Build a complete candidate outside the target.
3. Run `python3 scripts/validate_career.py <candidate>`; partial but structurally valid databases are allowed.
4. Do not replace the target while errors remain.
5. Re-read and reconcile any concurrent target change.
6. Apply the candidate through a patch or safe atomic replacement.
7. Run `make check` on the final repository.

Use `python3 scripts/validate_career.py --require-complete` only when a downstream resume workflow requires roles and skills. Report changed records, estimates, unverified claims, disclosure exceptions, follow-ups, and validation results. Update `Last reviewed` only after a successful factual update or completed review.
