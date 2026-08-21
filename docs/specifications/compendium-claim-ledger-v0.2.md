# Compendium Claim Ledger v0.2

**Status:** candidate boundary spec  
**Implementation priority:** deferred behind manuscript foundation

## Purpose

The Compendium is a manuscript-subordinate continuity sidecar. It answers what the manuscript says about an entity, where, under which scope, with what evidence, and whether it conflicts.

## Core objects

- Entity: stable thing or concept.
- Relation: typed connection.
- Claim: atomic assertion and the sole owner of its canon state.
- Evidence: support, contradiction, context, or inference locator.
- Conflict: incompatible claims in overlapping scope.
- Canon state: `candidate`, `active`, `locked`, `publication_locked`, `alternate`, `contradicted`, `deprecated`, or `rejected`.

## Canon-state authority

Canon state is stored as `claim_record.canon_state`. There is no separate canonical Canon State record in the F1 model.

This keeps the decision about whether an assertion is candidate/active/locked/etc. attached to the assertion it governs and prevents a second state object from becoming a competing authority. Entity lifecycle state remains separate and answers whether the Entity record itself is a stub, candidate, active, locked, deprecated, or merged.

The Claim schema imports the shared `CanonState` enum. Graph/search projections may mirror canon state but may not mutate it independently.

## Governance

Manual, observed, inferred, and imported bases remain distinct. AI extraction creates candidate records through PatchSession. Nothing inferred becomes active or locked canon without review, and canon-state changes are canonical mutations governed by the Mutation Envelope.

## Minimal first implementation

- Entity stubs
- Manual claims
- Evidence anchors into Sheets
- Current-Sheet entity and claim inspector
- Basic conflict records
- Search by entity, claim canon state, evidence, and manuscript scope

Graph projection, automated series-wide continuity scans, motif maps, and franchise dashboards remain derived and deferred.
