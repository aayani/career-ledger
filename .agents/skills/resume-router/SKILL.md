---
name: resume-router
description: Route every request to generate, update, or tailor a resume or CV before invoking resume-cover-letter. Present the supported resume scopes, collect only the route-specific input, and hand the selected scope to the writer. Do not use for cover-letter-only requests or career-history intake.
user-invocable: false
disable-model-invocation: false
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

Read `data/profile.yaml` and run `make validate-complete`. Resolve validation errors before drafting. Inspect the relevant existing resume files under `docs/resume/`, and ask only for material facts or preferences unavailable from those sources.

Determine the target market from the vacancy or request. Support Sweden/EU and other markets in addition to AU/NZ, US, and UK; ask only when regional convention materially changes the result.

## Shape the target before drafting

Read [tailoring.md](references/tailoring.md) before every handoff. For **particular position** and **specific role**, build its requirement map and pass the map, top priorities, and genuine gaps to the writer. For **general**, apply only its emphasis rules.

## Handoff to the writer

Invoke `resume-cover-letter` with the selected scope, repository evidence, target market, existing variant when applicable, and unresolved inputs. Apply the scope contract above instead of the writer's generic input defaults, and do not ask again for background already supported by `data/profile.yaml`.

Create and update resume deliverables under `docs/resume/`. Do not use the repository-root `resume/` directory.

## Review before delivery

Before presenting or saving any resume, run every check in [review.md](references/review.md) against `data/profile.yaml`. Correct failures in the draft, then report remaining gaps, assumptions, and approximate values to the user.

Before overwriting an existing variant, ask whether the user has submitted it. If so, create a new variant so the submitted version stays available for later interview rounds.
