# Canonical Career Evidence Database

This template defines the repository's human-editable source of truth for career facts. It is deliberately not resume-ready prose. Resumes, cover letters, portfolio copy, and interview stories should select and adapt facts from this database without strengthening uncertain claims.

## Schema rules

- Keep records neutral, factual, and region-independent.
- Use `YYYY-MM` for employment, projects, certifications, and career breaks.
  Education may use `YYYY` where month precision adds no value.
- Use `Present`, `Unknown`, `Not documented`, and `Not applicable` exactly.
- Give every role, achievement, education, project, activity, skill, and follow-up record a unique semantic ID. IDs use lowercase letters, numbers, and hyphens and begin with the record type, for example `role-example-engineer-2024` or `ach-example-api-latency`.
- Never change an ID merely because display wording changes.
- Required fields must remain present. Remove empty optional fields and empty optional sections instead of leaving placeholders.
- `Verification` is one of `Verified`, `Estimated`, or `Unverified`.
- `Ownership` is one of `Lead`, `Primary`, `Shared`, `Contributor`, or `Support`.
- The database default is application-safe. Add `Disclosure: Interview-only` or `Disclosure: Do not disclose` only for an exception.
- `Evidence` contains a short private reference or provenance note, never confidential documents, credentials, internal URLs, customer data, or employer-sensitive material.
- `Skills` contains comma-separated skill IDs defined in the Skills index.
- `Tags` uses lowercase kebab case. Prefer the namespaces `function-`, `seniority-`, `domain-`, and `evidence-`; other semantic tags are allowed.
- Missing facts use an explicit controlled value and receive a follow-up item when resolving them would materially improve an application.

## 1. Database metadata

- Schema version: 1.0
- Last reviewed: [YYYY-MM-DD]
- Default disclosure: Application-safe
- Language policy: Region-neutral English

## 2. Identity

- Name: [Full name]
- Location: [City, country]
- Email: [Email]
- Phone: [Phone]
- LinkedIn: [URL]
- GitHub: [URL]
- Portfolio: [URL]

## 3. Positioning facts

- Career start: [YYYY-MM]
- Primary specializations: [Facts]
- Secondary specializations: [Facts]
- Differentiators: [Facts]
- Leadership scope: [Facts]
- Industry experience: [Facts]

Do not store a narrative professional summary. Generate one for each target
role from these positioning facts and the evidence records below.

## 4. Experience

List employers in reverse chronological order. Group multiple positions under
one employer.

### [Employer]

#### [Position]

- ID: role-[employer]-[position]-[start-year]
- Employer: [Employer]
- Title: [Position]
- Location: [City, country]
- Employment type: [Permanent, Contract, Internship, Self-employed, or Not documented]
- Start: [YYYY-MM]
- End: [YYYY-MM or Present]
- Career stage: [Early, Professional, or Not documented]
- Scope: [Neutral description of ongoing ownership; maximum 80 words]
- Responsibilities:
  - [Recurring responsibility]
- Skills: [skill-id, skill-id]
- Technologies: [Comma-separated technologies]
- Practices: [Optional comma-separated engineering practices]
- Tags: [Controlled and optional semantic tags]

##### [Achievement title]

- ID: ach-[employer]-[semantic-description]
- Context: [Problem, constraint, or opportunity]
- Contribution: [Concrete work performed]
- Outcome: [Measured or accurate qualitative change]
- Scope: [Product, system, team, users, or other boundary]
- Ownership: [Lead, Primary, Shared, Contributor, or Support]
- Skills: [skill-id, skill-id]
- Tags: [Controlled and optional semantic tags]
- Verification: [Verified, Estimated, or Unverified]
- Evidence: [Private reference or provenance note]
- Disclosure: [Optional exception only]

Keep achievement records concise; validation warns above 130 words. Do not split
`Context` and `Contribution` merely to restate the same sentence.

## 5. Education

### [Qualification]

- ID: edu-[institution]-[qualification]
- Institution: [Institution]
- Location: [City, country]
- Start: [YYYY]
- End: [YYYY or Unknown]
- Focus: [Relevant study areas]
- Awards: [Awards or Not applicable]
- Verification: [Verified, Estimated, or Unverified]
- Evidence: [Private reference or provenance note]

## 6. Certifications and licenses

Omit this section when there are no records.

### [Certification]

- ID: cert-[issuer]-[certification]
- Issuer: [Issuer]
- Issued: [YYYY-MM]
- Expires: [YYYY-MM, Does not expire, or Unknown]
- Credential ID: [ID or Not documented]
- Credential URL: [URL or Not documented]
- Verification: [Verified, Estimated, or Unverified]
- Evidence: [Private reference or provenance note]

## 7. Projects

### [Project]

- ID: project-[semantic-name]
- Start: [YYYY-MM or Unknown]
- End: [YYYY-MM, Present, or Unknown]
- Status: [Active, Complete, Paused, or Not documented]
- Purpose: [Problem or user need]
- Contribution: [Personal contribution]
- Outcome: [Measured or qualitative result]
- Collaborators: [Names, team description, Solo, or Not documented]
- URL: [URL or Not documented]
- Repository: [URL or Not documented]
- Skills: [skill-id, skill-id]
- Technologies: [Comma-separated technologies]
- Tags: [Controlled and optional semantic tags]
- Verification: [Verified, Estimated, or Unverified]
- Evidence: [Private reference or provenance note]

## 8. Other professional activities

Use this schema for open source, awards, speaking, publications, volunteering,
and professional memberships. Omit empty categories.

### [Activity]

- ID: activity-[semantic-name]
- Type: [Open source, Award, Speaking, Publication, Volunteering, or Membership]
- Organization: [Organization or Not applicable]
- Date: [YYYY-MM, YYYY, or Unknown]
- Contribution: [Fact]
- Outcome: [Result or Not documented]
- URL: [URL or Not documented]
- Skills: [skill-id, skill-id, or Not applicable]
- Verification: [Verified, Estimated, or Unverified]
- Evidence: [Private reference or provenance note]

## 9. Languages

- [Language]: [Native, Professional, Working, Elementary, or Not documented]

## 10. Career breaks

Omit this section when there are no relevant records.

### [Career break title]

- ID: break-[semantic-name]
- Start: [YYYY-MM]
- End: [YYYY-MM]
- Description: [Accurate, concise fact]
- Activities: [Study, caregiving, travel, volunteering, or Not documented]

## 11. Skills index

Do not assign subjective proficiency levels. Evidence and recency should allow an output generator to infer the appropriate emphasis.

### [Skill or capability]

- ID: skill-[semantic-name]
- Category: [Backend, Frontend, Cloud, Data, Quality, Operations, Leadership, or other]
- First used: [YYYY-MM, YYYY, or Unknown]
- Last used: [YYYY-MM, YYYY, Present, or Unknown]
- Context: [Production, Commercial, Academic, Personal, or Mixed]
- Capabilities: [Specific technologies and practices represented by this record]
- Evidence: [Comma-separated role, achievement, project, or activity IDs]

## 12. Data-quality follow-up

### [Short issue title]

- ID: followup-[semantic-name]
- Related records: [Comma-separated IDs]
- Priority: [High, Medium, or Low]
- Issue: [Missing, conflicting, or weakly supported fact]
- Resolution: [Specific information or reference needed]
- Status: [Open or Resolved]
