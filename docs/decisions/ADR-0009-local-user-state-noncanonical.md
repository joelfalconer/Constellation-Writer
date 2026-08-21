# ADR-0009: Keep cursor, scroll, panes, and recent context outside canonical project metadata

- Status: accepted
- Decision class: medium-high reversal cost
- Review gate: F1
- Accepted at: F1 architecture-coherence adversarial closure

## Context

Earlier Sheet drafts placed cursor and scroll fields in canonical sidecars. These fields change frequently, create sync churn, differ by user/device, and do not describe manuscript truth.

The serious rival is portable canonical context state for cross-device continuity. That convenience does not justify making volatile device/user state part of manuscript truth.

## Decision

Store cursor, scroll, pane layout, recent context, and equivalent interaction state under `.workbench/user-state/<local-user-id>/` or an equivalent app-local store. It is ephemeral or recoverable and safe to delete from the perspective of project truth.

Recovery-critical unsaved text remains in dedicated recovery buffers, not ordinary user state.

A later portable handoff/context record may exist, but it must be explicitly exported or synchronized, optional, user-scoped, and non-authoritative.

## Consequences

- Cleaner canonical diffs and fewer sync conflicts.
- Projects open portably without a prior device state.
- Recent context may be absent after copying a project, which requires a deterministic fallback.
- Multi-device continuity must be designed as an optional projection/handoff capability rather than smuggled into canonical Sheet metadata.

## Falsifier

Revise if professional handoff or multi-device continuation cannot meet product requirements without a portable context record. Even then, the record must remain optional and non-authoritative unless a future explicit governance decision changes canonicality.

## F2 checks

- deleting all user-state files does not alter manuscript/project interpretation;
- user-state writes never modify Sheet or Manifest revision digests;
- recovery buffers are distinguishable from ordinary cursor/pane state;
- opening a copied project with no user state has a deterministic safe fallback;
- any future handoff record can be discarded without loss of project truth.
