# Agent Instructions

## Communication

- Be light, friendly, reassuring, direct, and concise.
- Ask questions without preambles. Format choices as `(1)`, `(2)`, `(3)`.
- Do not narrate internal steps or execution.

## Session

- At the start of each session, run `python3 scripts/init_session.py` before anything else. Let `<session>` be the exact directory it prints; reuse it for the entire session.
- Track progress in `<session>/checklist.md`. Store all notes, plans, temporary or working files, logs, exports, and generated artifacts in `<session>/artifacts/`.
- Edit canonical repository files only when the task requires it.
- Never read or write outside the repository root. Stop and ask if external access is required.

### Checklist

Process checklist items from top to bottom:

1. Complete the next applicable `[ ]` item, then mark it `[x]`.
2. Mark inapplicable items `[-]`.
3. Mark a blocked item `[!]` and stop.
4. Do not start a later item while an earlier item is `[ ]`.
5. In alternative or mode sections, complete the selected section and mark all others `[-]`.

## Skills

- Repository skills live only in `.agents/skills/` and use the portable Agent Skills format.
- Before each request, inspect every `.agents/skills/*/SKILL.md` frontmatter. When a description matches, read that `SKILL.md` completely and follow it; read linked resources only when directed.
- Do not create provider-specific copies under `.claude/`, `.github/`, `.codex/`, or similar directories.
- Do not modify third-party or vendored skills unless explicitly asked. Add repository-specific behavior through a repository-owned wrapper or companion skill.

### Available

#### Custom

- `career-ledger`
- `resume-router`
- `resume-validator`

#### Third-Party

- `resume-cover-letter`
