# Agent Instructions

## Conversation style

- Tone: Assuring and light hearted
- Be straightforward
- Use minimum words
- Ask the question directly
- If the user needs to presented with choices; use numbered options like (1), (2), (3) etc.
- User is not interested in what you are doing or what skill you are using, so maintain radio silence while working.

## Skills

Repository-local skills live in `.agents/skills/` and follow the portable Agent Skills format.

Before working on a request, inspect the frontmatter in each `.agents/skills/*/SKILL.md`. When a skill's description matches the request, read that `SKILL.md` completely and follow its instructions. Read linked resources only when the skill directs you to them.

Keep `.agents/skills/` as the single source of truth. Do not create agent-specific copies under `.claude/`, `.github/`, `.codex/`, or similar provider directories.

Do not modify third-party or vendored skills unless the user explicitly asks to update that specific skill. When repository-specific behavior is needed, prefer a repository-owned wrapper or companion skill.

### Available Skills

#### Custom Skills

- `career-timeline`
- `resume-router`

#### Third-Party Skills

- `resume-cover-letter`

Discover current descriptions and routing boundaries from each skill's frontmatter.
