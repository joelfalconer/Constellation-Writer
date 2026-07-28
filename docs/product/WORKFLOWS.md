# Core Workflow Catalogue v0.1

Each workflow names canonical effects, derived effects, recovery, and the expected return state.

## WF-001 Create project

**Intent:** begin a durable local project.  
**Canonical writes:** project manifest, default manuscript manifest, first Sheet and sidecar.  
**Derived writes:** catalog and recent-project entry.  
**Recovery:** operation plan and rollback if creation fails midway.  
**Done:** editor opens first Sheet with local save confirmed.

## WF-002 Resume writing

**Intent:** return to the latest meaningful context.  
**Canonical writes:** none until typing.  
**Derived reads:** local user state and recent context.  
**Fallback:** active manuscript first included Sheet.  
**Done:** cursor, scroll, and mode restored or fallback explained.

## WF-003 Draft and autosave

**Intent:** write without save administration.  
**Canonical writes:** atomic Sheet update with new revision.  
**Ephemeral state:** editor transaction and recovery buffer.  
**Failure:** buffer retained; save is not acknowledged.  
**Done:** current revision hash verified.

## WF-004 Split Sheet

**Intent:** divide a durable writing unit at the cursor.  
**Canonical writes:** source Sheet, new Sheet, sidecars, affected manifests.  
**Governance:** high-consequence Mutation Envelope with preview.  
**Recovery:** pre-operation bundle.  
**Done:** prose order preserved and cursor placed in chosen result.

## WF-005 Reorder manuscript

**Intent:** move a placement without touching prose.  
**Canonical write:** manuscript manifest only.  
**Derived writes:** binder and compile-plan mirrors.  
**Done:** new order visible and compile preview marked stale.

## WF-006 Search and return

**Intent:** recover known or half-remembered material.  
**Canonical writes:** none unless a saved search is created.  
**Derived reads:** FTS, structural catalog, recent context, optional semantic index.  
**Done:** result opens with query preserved and Return restores origin.

## WF-007 Compile draft

**Intent:** produce a deterministic manuscript artifact.  
**Canonical writes:** none unless saving profile changes.  
**Logged writes:** compile receipt and optional publication archive.  
**Done:** artifact, QA report, and source map share one compile ID.

## WF-008 Review AI patch

**Intent:** inspect a proposed transformation.  
**Canonical writes:** none before acceptance.  
**Review:** accept, edit, partially accept, reject, or defer.  
**Application:** Mutation Envelope checks base revisions and writes atomically.  
**Done:** outcome and provenance logged; editor returns to affected span.

## WF-009 Resolve external conflict

**Intent:** reconcile two valid divergent versions.  
**Canonical writes:** chosen merge or preserved separate Sheets after review.  
**Recovery:** base, current, and external versions retained.  
**Done:** conflict receipt records decision and restoration path.

## WF-010 Restore

**Intent:** recover from snapshot, archive, buffer, or patch history.  
**Precondition:** source integrity checked.  
**Governance:** pre-restore snapshot and preview.  
**Done:** restored objects validate and indexes rebuild.

## Workflow acceptance format

Every implementation workflow test records:

```yaml
workflow_id: WF-...
starting_state: {}
canonical_changes: []
derived_changes: []
recovery_artifacts: []
return_state: {}
result: pass|fail|partial
```
