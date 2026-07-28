# ADR-0008: Store annotations in dedicated append-oriented logs

- Status: proposed
- Decision class: high reversal cost
- Review gate: F1/F2 boundary

## Context

Inline comments maximize portability but pollute prose. Sheet-sidecar comments make sidecars volatile and conflict-heavy. Comments also need history, provenance, re-anchoring, resolution, and optional export.

## Decision

Use `annotations/<sheet-id>.annotations.jsonl` as the canonical annotation event stream, with optional compacted snapshots and optional portable inline syntax for interchange.

Sheet sidecars hold Sheet metadata, not comment history. SQLite mirrors current annotation state.

## Consequences

- Clean Markdown bodies and calmer sidecars.
- Append-oriented history and review provenance.
- More files and a compaction/migration responsibility.
- Sheet split/merge operations must redistribute or re-anchor annotation events through review.

## Falsifier

Revise if file-count and sync behavior materially outweigh history/recovery benefits in reference-project testing.
