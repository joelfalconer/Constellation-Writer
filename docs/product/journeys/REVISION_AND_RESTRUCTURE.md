# Journey: Revision and Restructure

## Goal

Change wording and large-scale structure while preserving control, comparison, and reversibility.

## Journey

1. Enter Revise mode without changing source representation.
2. Inspect comments, style warnings, or proposed patches only when summoned.
3. Accept or reject individual suggestions.
4. Reorder scenes in the manuscript binder without touching Sheet prose.
5. Exclude cut material without deleting it.
6. Compile a review draft and inspect QA.
7. Revert a bad accepted patch or restore a pre-operation snapshot.

## Critical distinctions

- Sheet identity versus manuscript placement;
- source text versus analysis overlay;
- proposed patch versus applied mutation;
- excluded versus deleted material.

## Acceptance measures

- hunk-level acceptance eventually supported;
- stale patches cannot blind-apply;
- manifest reorder leaves Sheet hashes unchanged;
- reversal creates a logged recovery event.
