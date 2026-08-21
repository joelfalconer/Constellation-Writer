# Mutation Envelope v0.1

**Status:** accepted F1 architecture contract; executable validation pending F2  
**Imports:** `INV-MUT-001`, `INV-REC-001`, identity, revision, anchor, provenance, consequence contracts  
**Decision:** ADR-0007

## Purpose

The Mutation Envelope is the shared transaction contract beneath autosave, human commands, AI PatchSessions, imports, batch refactors, migrations, conflict resolution, and restore.

PatchSession is the review-facing container. Recovery supplies preservation and rollback material. The Mutation Envelope ensures both use one application model rather than neighbouring protocols.

## Authority

The Mutation Envelope is the sole canonical application authority. It owns preflight, canonical write application, resulting revision creation/validation, outcome recording, and links to recovery artifacts.

It does **not** own proposal/editorial review or recovery storage:

- PatchSession owns review-bearing proposal, provenance, and acceptance/rejection state.
- Recovery owns buffers, snapshots, bundles, conflict copies, and restore preparation.
- Restore itself is applied as a new Mutation Envelope operation.
- Mutation event logs record outcomes but do not independently apply canonical writes.

## Contract

```yaml
operation_id: op_uuidv7
source:
  kind: human|ai|script|import|migration|recovery|system
  actor_id: string
intent: string
consequence: transient|canonical_low|canonical_high|destructive

targets:
  - object_id: string
    object_type: string
    base_revision_id: string
    base_hash: sha256
    anchor: optional_anchor

proposed_changes:
  format: unified_diff|json_patch|object_merge|file_operation|generated_record
  body: object_or_string

preconditions:
  - target_exists
  - revision_matches
  - target_not_locked
  - schema_valid
  - sufficient_disk_space

review:
  required: boolean
  state: not_required|pending|accepted|rejected|partial
  reviewer: string|null

recovery:
  strategy: undo|inverse_patch|recovery_bundle|snapshot
  snapshot_id: string|null

application:
  state: proposed|preflight|applying|applied|failed|reverted
  resulting_revisions: []

provenance: provenance_object
audit_events: []
```

## Consequence policy

| Level | Examples | Review | Recovery |
|---|---|---|---|
| transient | pane state, search, preview | none | none |
| canonical_low | rename, label, direct save | implicit human authority | undo or inverse |
| canonical_high | bulk reorder, large patch | explicit preview | recovery bundle or snapshot |
| destructive | delete, migration, overwrite resolution | explicit confirmation | mandatory snapshot |

Any AI-originated canonical mutation requires explicit review regardless of apparent consequence.

## Autosave rule

The shared model must not turn every keystroke into a heavyweight transaction. The editor buffer remains immediate. Debounced/background persistence may coalesce writer-originated changes into a lightweight `canonical_low` envelope with implicit human authority and consequence-proportional recovery.

If the envelope cannot support that without blocking the writing loop, ADR-0007 must be reopened.

## Application protocol

1. Resolve stable targets.
2. Validate base revisions and anchors.
3. Validate schema and locks.
4. Create required recovery artifact.
5. Apply writes atomically where possible.
6. For multi-file operations, follow a written operation plan.
7. Validate resulting canonical state.
8. Append outcome events.
9. Rebuild affected derived projections.
10. Expose a reversal route when promised.

## Failure behavior

A failed multi-file operation is never reported as clean. The envelope records completed, failed, and restored targets and routes the project into recovery review where needed.

## Acceptance tests

- AI cannot bypass PatchSession review and the envelope to write canonical files.
- A stale base revision blocks blind application.
- A destructive operation has a pre-operation snapshot.
- A partially failed operation can be rolled back or completed from its recovery bundle.
- Reversal creates a new logged mutation rather than deleting history.
- Restore is applied through the same canonical application model.
- Direct/autosave persistence does not block the editor interaction loop.
- Deleting derived indexes cannot create a competing write path during rebuild.
