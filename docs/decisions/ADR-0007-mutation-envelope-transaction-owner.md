# ADR-0007: Mutation Envelope owns canonical transaction application

- Status: proposed
- Decision class: high reversal cost
- Review gate: F1

## Context

Autosave, PatchSession, imports, migrations, batch refactors, conflict resolution, and restore all require preconditions, operation plans, atomic writes, validation, receipts, and rollback. Earlier component drafts risked giving PatchSession and Recovery competing transaction ownership.

## Decision

The Mutation Envelope is the shared operation and transaction contract.

- PatchSession owns proposal review, provenance, acceptance, and editorial decision.
- Mutation service owns preflight, application, revision creation, verification, and inverse/recovery references.
- Recovery owns buffers, snapshots, recovery bundles, conflicts, and restore mechanisms.

## Consequences

- One canonical mutation path can enforce revision and lock checks.
- PatchSession does not need to become an event-sourced filesystem engine.
- Autosave can use the same substrate with a consequence-specific authorization policy.
- Multi-file atomicity remains recovery-backed rather than magically transactional.

## Falsifier

Reject or revise if the shared envelope adds blocking overhead to ordinary typing or cannot model low-latency autosave cleanly.
