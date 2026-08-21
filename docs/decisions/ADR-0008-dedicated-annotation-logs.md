# ADR-0008: Store annotations in dedicated append-oriented logs

- Status: deferred pending F2 validation
- Decision class: high reversal cost
- Review gate: F1/F2 boundary

## Context

Inline comments maximize portability but pollute prose. Sheet-sidecar comments make sidecars volatile and conflict-heavy. Comments also need history, provenance, re-anchoring, resolution, and optional export.

## Candidate direction

Use `annotations/<sheet-id>.annotations.jsonl` as the canonical annotation event stream, with optional compacted snapshots and optional portable inline syntax for interchange.

Sheet sidecars hold Sheet metadata, not comment history. SQLite mirrors current annotation state.

## Why F1 does not accept this yet

The direction creates no competing F1 authority, so it does not block Architecture Coherent. But its actual fitness depends on behavior that has not yet been exercised: file-count growth, generic file-sync conflict behavior, append/compaction semantics, Sheet split/merge redistribution, anchor re-resolution, and import/export portability.

Accepting the storage format before those tests would convert a design preference into durable schema authority too early.

## Consequences if later accepted

- Clean Markdown bodies and calmer sidecars.
- Append-oriented history and review provenance.
- More files and a compaction/migration responsibility.
- Sheet split/merge operations must redistribute or re-anchor annotation events through review.

## F2 acceptance assay

- create and resolve large annotation sets across multiple Sheets;
- edit the same annotation stream through realistic external-sync conflict fixtures;
- split and merge Sheets while preserving/re-anchoring comments with explicit confidence;
- compact an event stream and prove equivalent current annotation state;
- export/import portable inline annotations without making inline syntax canonical;
- delete/rebuild SQLite and recover the same annotation state from canonical files alone.

## Falsifier

Reject or revise if file-count, sync behavior, compaction cost, or re-anchoring failure materially outweighs history/recovery benefits in the executable reference project.
