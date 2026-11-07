---
name: resume-validator
description: Review generated Markdown resumes for natural language, missing information or career gaps, impact, consistency, and ATS readability. Use after Markdown resume generation or when the user asks to validate, critique, or quality-check a Markdown resume.
user-invocable: true
disable-model-invocation: false
argument-hint: "[resume.md]"
---

# Resume Validator

Review only; do not rewrite the resume.

## Checks

Score these locked metrics in this order. Do not add, rename, or omit metrics.

1. `human_readability`: Jargon, keyword stuffing, vague claims, unnatural phrasing, repetition, and AI-sounding vocabulary.
2. `completeness`: Missing essentials, unexplained timeline gaps, weak context, and unsupported claims. Do not invent facts.
3. `impact`: Dull or duty-only bullets; strength of actions, outcomes, scope, and evidence.
4. `consistency`: Conflicting dates, titles, tense, terminology, formatting, or chronology.
5. `ats_readiness`: Standard headings, plain structure, chronology, keyword alignment, readable contact details, and parsing risks such as tables, columns, icons, or embedded HTML.

## Output

Return only JSON matching:

```ts
// Return only this array as JSON. Do not include a verdict or surrounding text.
{
  "metric": "human_readability" | "completeness" | "impact" | "consistency" | "ats_readiness"; // Locked metric name.
  "score": number; // Integer from 1–100: 1 means severe problems; 100 means no material problems.
  "feedback": { // Findings for this metric; use an empty array when there are none.
    "reason": string; // Specific evidence explaining the issue.
    "suggestion": string; // Actionable way to fix the issue.
    "priority": number; // Integer from 1–10, where 10 is most urgent.
  }[];
}[]
```
