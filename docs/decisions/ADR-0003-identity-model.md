# ADR-0003: Four-Part Identity Model

**Status:** proposed

## Decision

The architecture distinguishes object identity, placement identity, revision identity, and anchor identity.

## Model

- Object ID: enduring Sheet, Entity, Claim, Manuscript, or other domain object.
- Placement ID: a particular location of an object in an assembly.
- Revision ID: a validated state of an object.
- Anchor: a span or structure within an object revision.

## Rationale

This distinction supports Sheet reuse, alternate cuts, comments, evidence, AI patches, conflict resolution, snapshots, and compile source maps without conflating title, path, order, and text position.

## Revisit trigger

The exact identifier format may change before public data exists. The conceptual separation must remain.
