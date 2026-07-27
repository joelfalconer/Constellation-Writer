# Concept Glossary

## Sheet

The smallest durable unit of authorship. A Sheet has stable object identity, readable text, and local metadata. It is not its filename, title, path, or manuscript placement.

## Manuscript

A directed assembly of placements that reference Sheets. The manuscript manifest owns order, nesting, inclusion, and structural role.

## Placement

A node representing one Sheet or structural object at a particular location in a manuscript. Placement identity differs from Sheet identity.

## Revision

A particular validated state of a canonical object, identified by revision ID and content hash.

## Anchor

A locator for a span or structure within a particular object revision. Anchors may combine quoted text, structural path, and positional hints.

## Canonical state

Durable current project truth stored in inspectable files.

## Logged state

Durable event or history truth, including mutations, migrations, conflicts, snapshots, and publication locks.

## Derived state

Rebuildable projections including SQLite mirrors, search indexes, graph projections, embeddings, previews, and statistics.

## Mutation Envelope

The shared contract governing intent, actor, targets, base revisions, proposed changes, review, application, recovery, provenance, and outcome.

## PatchSession

The writer-facing review and provenance container for one or more proposed or applied mutations.

## Compile Profile

A canonical output contract defining inclusion overrides, semantic transformations, style maps, QA rules, and target format.

## Claim

An atomic assertion about an entity, event, relation, rule, motif, timeline, or publication state.

## Evidence

A durable locator showing what supports, contradicts, contextualizes, or implies a Claim.

## Compendium

A manuscript-subordinate continuity sidecar for entities, claims, evidence, relations, canon states, and conflicts.
