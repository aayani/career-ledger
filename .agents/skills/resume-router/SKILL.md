---
name: resume-router
description: Route every request to generate, update, or tailor a resume or CV before invoking resume-cover-letter. Present the supported resume scopes, collect only the route-specific input, and hand the selected scope to the writer. Do not use for cover-letter-only requests or career-history intake.
---

# Resume Router

Run this repository-owned adapter before `resume-cover-letter` whenever the requested deliverable includes a resume or CV. Cover-letter-only requests bypass it.

## Select the scope

Use an unambiguously requested scope without repeating the menu. Otherwise ask exactly:

> What should be the scope of the resume?
>
> (1) General  
> (2) For a particular position (paste link or job description)  
> (3) For a specific role

Gather only the missing route input: the vacancy URL or description for **particular position**, or the target role for **specific role**. **General** needs neither a vacancy nor a company.

## Use repository evidence first

Read `docs/career.md` and run `python3 scripts/validate_career.py docs/career.md --require-complete`. Resolve validation errors before drafting. Inspect the relevant existing resume files under `docs/resume/`, and ask only for material facts or preferences unavailable from those sources.

Determine the target market from the vacancy or request. Support Sweden/EU and other markets in addition to AU/NZ, US, and UK; ask only when regional convention materially changes the result.

## Handoff to the writer

Invoke `resume-cover-letter` with the selected scope, repository evidence, target market, existing variant when applicable, and unresolved inputs. The route overrides the writer's generic input defaults:

- **General** does not require a company or vacancy.
- **Specific role** may target a role family without a company.
- Do not ask again for background already supported by `docs/career.md`.

Create and update resume deliverables under `docs/resume/`. Do not use the repository-root `resume/` directory.

For each resume, place `Personal Projects` after `Experience` only when at least one supported project strengthens the target, then place `Skills`. Include at most five projects, chosen for relevance, evidence, recency, and distinctiveness. Describe purpose, personal contribution, relevant technology, and outcome without inventing facts. Reconcile project technologies into `Skills`, remove unsupported or redundant entries, and keep terminology consistent.
