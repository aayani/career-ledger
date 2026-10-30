---
name: resume-router
description: Route resume or CV requests by scope, gather only missing inputs, and hand off to resume-cover-letter. Do not use for cover-letter-only requests or career-history intake.
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

## Review before delivery

Apply [review.md](references/review.md) before delivery. Correct failures and report remaining gaps, assumptions, and approximations. Preserve submitted variants by creating a new file.
