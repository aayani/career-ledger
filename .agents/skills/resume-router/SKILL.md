---
name: resume-router
description: Route resume or CV requests by scope, gather only missing inputs, hand off to resume-cover-letter, and validate generated Markdown resumes. Do not use for cover-letter-only requests or career-history intake.
user-invocable: false
disable-model-invocation: false
---

# Resume Router

Use before `resume-cover-letter` for every resume or CV request. Cover-letter-only requests bypass it.

## Select the scope

Use a clear requested scope. Otherwise ask:

> What should be the scope of the resume?
>
> (1) General
>
> (2) Particular position (paste link or description)
>
> (3) For a specific role

Gather only the vacancy for **particular position** or role name for **specific role**. **General** needs neither.

## Use repository evidence first

Read `data/profile.yaml`, run `make validate`, and inspect relevant files in `docs/resume/`. Resolve errors and ask only for missing material facts or preferences. Infer the market; ask only when regional convention matters.

## Shape the target before drafting

Read [tailoring.md](references/tailoring.md). Build a requirement map for targeted scopes; use only its emphasis rules for **general**.

## Handoff to the writer

Invoke `resume-cover-letter` with scope, evidence, market, existing variant, priorities, gaps, and unresolved inputs. Do not re-ask facts in `data/profile.yaml`. Save resumes under `docs/resume/`.

## Review and validate before delivery

1. Apply [review.md](references/review.md) and fix every failure.
2. Invoke `resume-validator` on the saved Markdown resume.
3. Stop when all metrics score 100, except `ats_readiness`, which may score 96–100.
4. Otherwise, fix supported findings, save, and revalidate. Never invent facts. Limit this to three revision cycles after the initial validation.
5. If it still fails, report the final findings and scores. Always report gaps, assumptions, and approximations, and preserve submitted variants in a new file.
