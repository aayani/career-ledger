# Resume Tailoring

Use this reference to decide what a resume should emphasize. It selects and frames facts from `data/profile.yaml`; it never adds facts.

## Requirement map

Build this map for **particular position** from the vacancy, and for **specific role** from the stated role family.

1. Extract from the source:
   - must-have requirements;
   - nice-to-have requirements;
   - critical keywords, such as tools, methods, and domain terms, in the source's exact wording;
   - seniority and scope signals;
   - the problem the role is hired to solve, when the source states it.
2. Map each requirement to supporting employment or skill IDs in `data/profile.yaml` and classify it:
   - **Direct:** a role, achievement, project, or activity demonstrates it;
   - **Transferable:** adjacent evidence supports it, with a clear bridge;
   - **Gap:** no record supports it;
   - **Unclear:** the source does not define it well enough to map.
3. Separate a missing keyword from a missing capability. When evidence exists under different wording, use the source's term only where it truthfully describes that evidence. Never add a keyword without a supporting record.
4. Select at most five priorities to lead the summary, the most recent roles, and `Skills`.
5. Report genuine gaps to the user instead of covering them. When the user may hold an unrecorded fact that would close a gap, offer to record it through `career-ledger` before drafting.

When the scope supplies a role but no vacancy, offer to either use the role family's common expectations or let the user provide a representative listing. Label role-family expectations as assumptions, and do not invent a company.

## Emphasis rules for every scope

- **Follow the reader's skim order.** Give the most detail to the current role and the previous one or two roles, unless an older record is the strongest evidence for the target. Keep the summary short and positioning-focused. Treat `Skills` as a searchable filter list, not a showcase.
- **Give each role a distinct purpose.** Before selecting bullets, privately complete "This role demonstrates the ability to..." for each role. Choose achievements that support that purpose and avoid repeating the same kind of claim across roles.
- **Curate skills by evidence.** List only skill groups and keywords supported by their project usage. Prefer specific keywords over generic ones, favour recent use, and omit tools or frameworks that were only incidental to the target.
- **Keep identity facts consistent.** Use the employers, titles, and dates exactly as recorded so the resume matches LinkedIn and other application material generated from the same database.

## Output structure

The following repository rules override the writer's generic section order:

- Associate projects in `employmentId` with their matching experiences without duplicating the same claim. Place independent projects under `Personal Projects` after `Experience` only when at least one strengthens the target, then place `Skills`.
- Include at most five projects, chosen for relevance, evidence, recency, and distinctiveness.
- Use each project's recorded situation, task, action, and result to describe its purpose, personal contribution, relevant technology, and result without inventing facts.
- Reconcile project technologies into `Skills`, remove unsupported or redundant entries, and keep terminology consistent.
