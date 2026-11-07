---
name: resume-validator
description: Review generated Markdown resumes for natural language, missing information or career gaps, impact, consistency, and ATS readability. Use after Markdown resume generation or when the user asks to validate, critique, or quality-check a Markdown resume.
user-invocable: true
disable-model-invocation: false
argument-hint: "[resume.md]"
---

# Resume Validator

Review only; do not rewrite the resume.

## Input

The Markdown resume to validate.

## Checks

Score these locked metrics in this order. Do not add, rename, or omit metrics.

1. `human_readability`: Jargon, keyword stuffing, vague claims, unnatural phrasing, repetition, and AI-sounding vocabulary.
2. `completeness`: Missing essentials, unexplained timeline gaps, weak context, and unsupported claims. Do not invent facts.
3. `impact`: Dull or duty-only bullets; strength of actions, outcomes, scope, and evidence.
4. `consistency`: Conflicting dates, titles, tense, terminology, formatting, or chronology.
5. `ats_readiness`: Standard headings, plain structure, chronology, keyword alignment, readable contact details, and parsing risks such as tables, columns, icons, or embedded HTML.

## Output

Read [references/feedback.ts](references/feedback.ts) and return only JSON matching its schema.
