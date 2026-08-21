# ADR-0007: Mutation Envelope owns canonical transaction application

- Status: accepted
- Decision class: high reversal cost
- Review gate: F1
- Accepted at: F1 architecture-coherence adversarial closure

## Context

Autosave, direct human commands, PatchSession, imports, migrations, batch refactors, conflict resolution, and restore all require some combination of preconditions, operation planning, canonical writes, validation, receipts, and recovery. Earlier component drafts risked giving PatchSession and Recovery neighbouring or competing transaction ownership.

That ambiguity is now a critical architecture question because Constellation Writer requires exactly one canonical application path for governed mutation while keeping ordinary writing responsive.

## Decision

The **Mutation Envelope is the sole shared application and transaction contract for canonical project mutation**.

Jurisdictions are deliberately separate:

- **PatchSession owns proposal, review, provenance, acceptance/rejection, and editorial decision.** It may contain or reference one or more proposed Mutation Envelopes, but it does not own filesystem transaction semantics.
- **Mutation service / Mutation Envelope owns preflight, authorization, application, revision creation, post-write validation, outcome recording, and recovery references.**
- **Recovery owns preservation and restoration mechanisms:** recovery buffers, snapshots, recovery bundles, conflict copies, rollback inputs, and restore workflows. Recovery does not become a second canonical write authority; restore is itself executed through a Mutation Envelope.
- **Mutation event/history records own durable outcome history.** They record what occurred; they do not independently apply writes.
- **Derived projections rebuild after a successful mutation and may never become an alternate source of canonical write authority.**

## Authority model

```text
human / AI / import / migration / recovery intent
                    |
                    v
          proposal or direct command
          (PatchSession when review-bearing)
                    |
                    v
             Mutation Envelope
     preflight -> recovery preparation -> apply
       -> validate -> outcome/revision record
                    |
          +---------+---------+
          |                   |
          v                   v
   canonical files      recovery/history
          |
          v
   derived projections rebuild
```

No subsystem may bypass this path for canonical mutation merely because its operation appears simple.

## Atomicity semantics

The Product Constitution's atomic-write law applies to **single-file canonical replacement** at the file boundary where the supported filesystem provides the required replacement primitive. The architecture does not pretend that a collection of ordinary filesystem writes automatically has database-style cross-file atomicity.

A multi-file Mutation Envelope therefore uses an explicit operation plan plus recovery artifacts. If interruption occurs after some file replacements have committed, the system must detect and disclose partial application, preserve enough information to complete or roll back safely, and enter recovery review where needed. It may not report the operation as atomically committed when that guarantee was not actually available.

If a future substrate provides genuine transactional multi-file semantics, the envelope may exploit them as an implementation optimization without changing the authority model.

## Autosave and latency

This decision does **not** require every keystroke to become a heavyweight transaction object. The editor buffer remains the immediate interaction surface. Autosave may use a lightweight `canonical_low` envelope with implicit human authority, coalescing, and minimal recovery bookkeeping.

The architecture is falsified if the shared envelope forces blocking work into the typing path or cannot support debounced/background persistence while preserving revision and recovery guarantees.

## Consequences

- One canonical mutation path can enforce revision, hash, lock, schema, and path-safety checks.
- PatchSession remains an editorial review/provenance object rather than an event-sourced filesystem engine.
- Recovery remains trustworthy without becoming a competing transaction protocol.
- Restore, migration, import, conflict resolution, bulk edits, AI acceptance, and ordinary save can share one consequence-sensitive substrate.
- Single-file canonical replacement is atomic where supported; multi-file consistency is recovery-backed unless the implementation can prove a stronger transactional guarantee.
- Outcome history becomes inspectable without making event replay necessary to reconstruct current canonical truth.

## Serious rivals considered

### PatchSession owns transaction application

Rejected. It fits AI/reviewed transformation but is the wrong abstraction for ordinary saves, migrations, imports, recovery restores, and human commands. Promoting it would make an editorial review container the universal storage engine and create pressure to bypass it for low-latency writes.

### Recovery owns transaction application

Rejected. Recovery must prepare and preserve rollback material, but making it the write authority collapses failure handling and ordinary mutation into one subsystem and creates a second route beside PatchSession/direct commands.

### Separate transaction models by subsystem

Rejected by hard gate. It creates competing canonical write semantics, inconsistent stale-base handling, and divergent recovery guarantees.

## Evidence and coherence basis

The accepted direction is consistent with:

- `docs/architecture/MUTATION_ENVELOPE.md`, which already defines the envelope beneath autosave, human commands, PatchSessions, imports, migrations, conflict resolution, and restore;
- `docs/specifications/patch-session-v0.2.md`, which explicitly makes PatchSession the writer-facing review/provenance container rather than the complete transaction model;
- `docs/specifications/recovery-backup-v0.2.md`, which defines single-file atomic replacement and recovery-backed multi-file operations;
- `docs/constitution/DEPENDENCY_RULES.md`, which forbids PatchSession and Recovery as competing transaction owners;
- `docs/constitution/SOVEREIGNTY_MODEL.md`, which requires every canonical write route to pass through a declared mutation policy;
- `INV-MUT-001`, which requires governed review for non-human canonical mutation.

This is an architecture-coherence decision. The Mutation Envelope is not yet accepted as production-tested substrate.

## Falsifiers and revisit triggers

Reopen this ADR if any of the following is observed in F2:

1. the envelope adds blocking latency to ordinary typing or debounced save;
2. autosave requires a materially different canonical write model to remain reliable;
3. restore or multi-file recovery cannot be represented without a second canonical application authority;
4. stale-base, lock, or revision checks become inconsistent across operation classes;
5. implementation introduces a canonical write path that bypasses the envelope and cannot be removed without unacceptable cost;
6. the supported filesystem/runtime cannot provide the single-file replacement guarantees assumed by the recovery design and no safe fallback can be defined.

## F2 acceptance tests

- direct human save uses the mutation substrate without blocking the editor interaction loop;
- AI cannot bypass PatchSession review and the Mutation Envelope to write canonical files;
- stale base revision blocks blind application;
- single-file replacement satisfies the documented atomic file-boundary behavior on supported filesystems;
- destructive operations obtain the required pre-operation recovery artifact;
- interrupted multi-file mutation exposes partial state and can recover or resume safely;
- restore is represented as a new governed mutation rather than silent filesystem replacement;
- derived indexes may be deleted/rebuilt and cannot write back around revision validation;
- mutation event history is inspectable but current canonical state does not require event replay.

## Reversal cost

High, but bounded before broad F2 implementation. Reversal after multiple subsystems independently implement the envelope would require contract migration across save, PatchSession, import, migration, recovery, conflict resolution, and derived-index invalidation. This is why sole application authority is locked at F1 while execution details remain falsifiable in F2.
