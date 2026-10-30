# Career Ledger

![Career Ledger turns verified career history into focused, application-ready resumes](docs/images/cover.jpeg)

A local-first career knowledge system for building a trusted professional history, generating focused resumes, and keeping every claim grounded in evidence.

[Why Career Ledger?](#why-career-ledger) · [How it works](#how-it-works) · [Get started](#get-started) · [Commands](#commands)

## Your career, without the guesswork

Career details are usually scattered across old resumes, profiles, documents, and memory. Career Ledger brings them together in one structured source of truth, then helps an AI coding agent turn that evidence into application-ready material without inventing facts or quietly strengthening uncertain claims.

Use it to:

- Capture roles, achievements, skills, projects, education, and career breaks;
- Distinguish verified facts from estimates and unverified claims;
- Preserve evidence, ownership, disclosure limits, and unresolved gaps;
- Generate general, role-focused, or vacancy-specific resumes;
- Export clean, ATS-friendly Markdown resumes to PDF.

> [!IMPORTANT]
> Imported resumes are treated as source material, not proof. Career Ledger keeps uncertainty visible until you confirm the facts.

## Why Career Ledger?

### One dependable career record

Maintain a canonical YAML database at `data/profile.yaml`. Stable education, employment, project, and skill IDs keep the history consistent as wording and skill usage evolve. Projects live in a separate root array and can optionally link to one or more employment records through an ID array.

### Evidence-aware by design

Projects use concise situation, task, action, and result fields of up to 100 characters each. Education, employment, and skill usages can be marked private, and honest qualitative results are preferred over invented metrics.

### Built for practical AI collaboration

Portable Agent Skills guide career intake and resume creation. Repository instructions keep supported coding agents aligned on the same workflows instead of relying on provider-specific copies.

### Quality gates included

The validator loads `schema.yaml` as JSON Schema Draft 2020-12 and checks required fields, formats, IDs, project employment links, controlled values, conditional education fields, privacy flags, and exact duplicates before career data reaches a resume.

The canonical schema lives at `.agents/skills/career-ledger/references/schema.yaml`.

### Application-ready outputs

Resume variants live in `docs/resume/`. The PDF workflow renders them into `output/` using a compact, single-column layout suitable for applicant tracking systems.

## How it works

![Career Ledger workflow from evidence collection through validation, tailored resume generation, and PDF export](docs/images/workflow.jpeg)

Career Ledger separates evidence from presentation. The profile stays neutral and reusable; each resume selects and adapts only the facts relevant to its audience.

## Get started

### 1. Fork the repository

The best way to use Career Ledger is to fork it and maintain your own copy. This gives you an independent career workspace while making it easy to pull in future improvements.

After forking the repository on GitHub, clone your fork:

```bash
git clone https://github.com/<your-github-username>/career-ledger.git
cd career-ledger
```

> [!CAUTION]
> Career records may contain personal information. Check your repository's visibility before committing real career data.

Python 3.10 or newer and [`uv`](https://docs.astral.sh/uv/) are required. Commands install their isolated dependencies on demand.

### 2. Build your career ledger

Open the repository with an AI coding agent that supports repository instructions and Agent Skills, then ask:

```text
Help me write my career timeline.
```

Choose either an existing resume import or a guided interview. The workflow creates `data/profile.yaml` and records material gaps as concise top-level notes.

### 3. Validate the evidence

```bash
make validate
```

### 4. Generate a resume

Ask your agent to generate a resume. Career Ledger routes the request to one of three scopes:

1. General
2. For a particular position using a vacancy link or job description
3. For a specific role

Resume source files are written to `docs/resume/`.

### 5. Export to PDF

```bash
make pdf path=docs/resume/backend.md
```

The PDF is written to `output/backend.pdf`. Pass `--output` directly to `scripts/markdown_to_pdf.py` when you need a custom destination.

## What the ledger captures

- Identity, contact details, and current location
- Employers and roles, plus separately stored projects with optional employment links
- Project descriptions and situation, task, action, and result narratives
- Education, courses, certifications, and licences
- Languages and evolving skill groups with tool and framework keywords
- Privacy flags for education, employment, and skill usages
- Free-form notes for career breaks and unresolved context

Project relevance is an independent integer score from 1 to 10. Skill-group IDs remain stable while names, keywords, and optional proficiency can vary by project usage.

## Commands

Inspect whether the profile is missing, empty, or populated:

```bash
make inspect
```

Validate the database:

```bash
make validate
```

Run the test suite:

```bash
make test
```

Run tests and validation together after `data/profile.yaml` exists:

```bash
make check
```

Treat warnings as failures in stricter automation:

```bash
make validate-strict
```

## Designed for trustworthy applications

Career Ledger is for professionals who want the speed of AI-assisted writing without losing control of accuracy. It keeps the durable facts separate from the final pitch, making it easier to tailor applications while preserving a clear, auditable foundation.

Improvements are welcome. If you have an idea for a workflow, validator, portability enhancement, or documentation update, open an issue or submit a pull request to the main repository.

## License

Career Ledger is available under the [MIT License](LICENSE).
