---
name: resume-validator
description: Review a Markdown resume at a supplied repository path for quality and completeness. Use after resume generation or for validation, critique, or quality checks.
user-invocable: true
disable-model-invocation: false
argument-hint: "[resume-path]"
---

# Resume Validator

Review only. Suggest fixes; do not rewrite the resume.

## Input

Accept exactly one input: the repository path to the saved Markdown resume.

Reject and stop without scoring if:

- The input is missing, contains multiple paths, or contains resume content.
- The path is outside the repository or is not a readable, regular `.md` file.

Return only a concise error on rejection. Otherwise, read and validate the file.

## Checks

Score these locked metrics in this order. Do not add, rename, or omit metrics.

1. `human_readability`: Jargon, keyword stuffing, vague claims, unnatural phrasing, repetition, and AI-sounding vocabulary.
2. `completeness`: Missing essentials, unexplained employment gaps longer than six months, and weak context. Essentials are the candidate's name, readable contact details, experience, skills, and education.
3. `impact`: Dull or duty-only bullets; strength of actions, outcomes, scope, and evidence.
4. `consistency`: Conflicting dates, titles, tense, terminology, formatting, or chronology.
5. `ats_readiness`: Standard headings, plain structure, chronology, keyword alignment, readable contact details, and parsing risks such as tables, columns, icons, or embedded HTML.

## Scoring

Start each metric at 100. Deduct every observable defect, including spelling and other minor errors:

- Minor: 1-3
- Moderate: 4-8
- Major: 9–20
- Severe: 21+

### Rules

- Each feedback item describes one observable defect, assigns its deduction as `score`, and gives a correction rather than an optional enhancement.
- Score each metric independently. When one defect affects multiple metrics, include it under every affected metric and explain its metric-specific effect.
- Without a job description, assess intrinsic ATS quality and add a 4-point deduction for unavailable keyword alignment to any other ATS deductions.
- Do not use praise as feedback.
- Do not invent facts.

### Invariants

- Metric score = 100 minus the sum of its feedback deductions.
- Keep total deductions between 0 and 99, so every metric score remains between 1 and 100.
- Feedback is empty if and only if the metric score is 100.

## Exceptions

Do not penalize:

- Clear repeated grammatical structures.
- Missing company descriptions.
- Quantified claims without resume citations.
- Past-tense achievements in a current role.
- Plain LinkedIn or GitHub URLs.

## Output

Read [references/feedback.ts](references/feedback.ts) and return only schema-compliant JSON. This indicates success; a rejection or error indicates failure.
