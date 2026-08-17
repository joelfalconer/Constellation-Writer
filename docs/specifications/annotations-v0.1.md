# Annotation and Comment Spec v0.1

## Purpose

Support editorial comments, revision issues, private notes, AI suggestions, and evidence-aware review without polluting Sheet bodies or conflating annotations with Sheet metadata.

## Canonical model

Annotations are append-oriented records stored separately from Sheet sidecars:

```text
annotations/<sheet-id>.annotations.jsonl
```

The current state is reconstructed from create, update, resolve, reopen, re-anchor, and delete-tombstone events. A compacted snapshot may be generated, but compaction must preserve provenance and recovery.

## Annotation kinds

- inline comment;
- margin annotation;
- revision issue;
- editorial note;
- AI suggestion note;
- compile issue reference;
- evidence review note.

## Required fields

```yaml
id: ann_...
sheet_id: sh_...
kind: revision_issue
status: open|resolved|dismissed
body: string
anchor: hybrid_anchor
created_at: timestamp
author_id: string
provenance: optional
export: false
```

## Anchor behavior

- Exact quote and revision are primary.
- Prefix, suffix, structural path, and line hints assist re-anchoring.
- Re-anchor confidence is recorded.
- A low-confidence or failed anchor becomes stale and requires review.
- The system never silently attaches a comment to unrelated text.

## Privacy and export

Annotations are excluded from normal manuscript compile by default. Compile profiles may include selected kinds for editor-review exports.

AI suggestion notes retain model/context provenance and remain candidates until a writer converts them into a normal annotation or patch.

## UI

Draft mode hides annotations by default. Revise mode may show margin markers and an Inspector list. Resolving an annotation does not remove its history.

## Edge cases

- Sheet split: propose annotation redistribution before applying the split.
- Sheet merge: preserve IDs and re-anchor against the merged revision.
- Deleted Sheet: retain orphan annotations for recovery and audit.
- External edit: re-anchor after revision scan and flag uncertainty.

## MVP

Create, edit, resolve, dismiss, jump, re-anchor, filter, and export-review annotations.
