# ADR-0009: Keep cursor, scroll, panes, and recent context outside canonical project metadata

- Status: proposed
- Decision class: medium-high reversal cost
- Review gate: F1

## Context

Earlier Sheet drafts placed cursor and scroll fields in canonical sidecars. These fields change frequently, create sync churn, differ by user/device, and do not describe manuscript truth.

## Decision

Store user/session state under `.workbench/user-state/<local-user-id>/` or an equivalent app-local store. It is ephemeral or recoverable and safe to delete from the perspective of project truth.

Recovery-critical unsaved text remains in dedicated recovery buffers, not ordinary user state.

## Consequences

- Cleaner canonical diffs and fewer sync conflicts.
- Projects open portably without a prior device state.
- Recent context may be absent after copying a project, which requires a deterministic fallback.

## Falsifier

Revise if professional handoff or multi-device continuation requires a carefully scoped portable context record. Such a record must remain optional and non-authoritative.
