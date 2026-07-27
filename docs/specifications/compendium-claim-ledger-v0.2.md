# Compendium Claim Ledger v0.2

**Status:** candidate boundary spec  
**Implementation priority:** deferred behind manuscript foundation

## Purpose

The Compendium is a manuscript-subordinate continuity sidecar. It answers what the manuscript says about an entity, where, under which scope, with what evidence, and whether it conflicts.

## Core objects

- Entity: stable thing or concept.
- Relation: typed connection.
- Claim: atomic assertion.
- Evidence: support, contradiction, context, or inference locator.
- Conflict: incompatible claims in overlapping scope.
- Canon state: candidate, active, locked, publication-locked, alternate, contradicted, deprecated, or rejected.

## Governance

Manual, observed, inferred, and imported bases remain distinct. AI extraction creates candidate records through PatchSession. Nothing inferred becomes active or locked canon without review.

## Minimal first implementation

- Entity stubs
- Manual claims
- Evidence anchors into Sheets
- Current-Sheet entity and claim inspector
- Basic conflict records
- Search by entity, claim status, evidence, and manuscript scope

Graph projection, automated series-wide continuity scans, motif maps, and franchise dashboards remain derived and deferred.
