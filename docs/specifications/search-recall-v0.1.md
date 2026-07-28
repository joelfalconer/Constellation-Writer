# Search and Recall Contract v0.1

## Purpose

Search is not one feature. It is a family of retrieval modes designed to recover text, structure, context, evidence, and half-remembered material without making a graph or AI system foundational.

## Search modes

| Mode | Source | Canonical? | Example |
|---|---|---:|---|
| literal | Sheet/source text via FTS or direct scan | no | exact phrase |
| structural | manifests and sidecars | no | excluded scenes in Part II |
| recent context | local user state | no | what I edited yesterday |
| metadata | sidecars and profiles | no | all Sheets marked revise |
| entity | Compendium records and mentions | no | appearances of Mara |
| claim/evidence | Claim Ledger | no | evidence for house rule |
| semantic | embedding projection | no | line about a house remembering |
| continuity | claims, scope, and conflicts | no | contradictions in current manuscript |

Search indexes are derived. Canonical files and records remain authoritative.

## Query contract

```yaml
query:
  text: string
  mode: auto|literal|structural|recent|metadata|entity|claim|semantic|continuity
  scope:
    project_id: prj_...
    manuscript_id: optional
    placement_id: optional
    sheet_ids: optional
  filters: {}
  created_at: timestamp
```

## Result contract

```yaml
result:
  object_id: stable_id
  object_type: sheet|placement|entity|claim|source|annotation
  locator: human_readable_location
  excerpt: text
  matched_span: optional_anchor
  mode: literal|structural|recent|metadata|entity|claim|semantic|continuity
  reason: explanation
  score: optional_number
  uncertainty: exact|high|medium|low
  return_token: local_state_reference
```

## Degraded modes

- Missing SQLite: direct project scan for literal and structural queries.
- Rebuilding FTS: show partial current results with state label.
- Missing embeddings: semantic mode unavailable; never block literal search.
- Stale graph: entity and claim records remain directly queryable.

## Ranking laws

- Exact matches outrank semantic similarity.
- Current manuscript and recent context may boost but cannot conceal stronger exact results.
- Semantic results are visibly labelled and explain the matched concept where possible.
- Search does not silently create links, tags, entities, or canon.

## Recall acceptance

- Find a known phrase across two million words within the performance budget.
- Recover a half-remembered line through semantic or lexical expansion without hiding literal alternatives.
- Open a result and return to the origin with query and selection intact.
- Produce the same structural result after deleting and rebuilding indexes.
