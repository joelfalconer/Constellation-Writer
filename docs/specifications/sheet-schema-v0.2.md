# Sheet Schema v0.2

**Status:** candidate  
**Imports:** object, revision, anchor, provenance contracts

## Definition

A Sheet is the smallest durable unit of authorship. Object ID is stable. Filename, title, path, heading, placement, and revision are distinct concepts.

## Ownership split

- Frontmatter: Sheet ID, schema marker, kind, optional portable title.
- Markdown body: prose.
- Sheet sidecar: canonical local metadata such as status, labels, goals, privacy, and default compile hints.
- Annotation log: comments, review notes, and anchored observations.
- Manuscript manifest: order, nesting, placement title, resolved structural role.
- Local user state: cursor, scroll, pane layout.
- SQLite: mirrors and derived indexes only.

## Minimum frontmatter

```yaml
---
id: sh_uuidv7
schema: constellation_sheet_v1
kind: manuscript
---
```

## Anchor compatibility

Comments, evidence, and patches use hybrid anchors containing object ID, revision ID, exact quote, context, and structural hints. Failed re-anchoring produces stale state rather than guessed application.

## Export precedence

Compile profile override → manuscript placement → Sheet default hint → Sheet-kind default.

## Acceptance tests

- Rename and move preserve identity.
- Duplicate IDs block ambiguous writes.
- Missing sidecar permits safe minimal recovery.
- External Markdown remains readable.
- Stale patch cannot apply blindly.
