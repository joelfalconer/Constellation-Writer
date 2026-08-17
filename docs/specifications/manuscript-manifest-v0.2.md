# Manuscript Manifest v0.2

**Status:** candidate  
**Imports:** `INV-ASM-001`, object and placement identity contracts

## Definition

A manuscript is a directed assembly of placement nodes that reference Sheets or structural objects. The manifest owns order, nesting, inclusion, placement titles, semantic compile roles, and structural break intent.

## Identity model

- Manuscript ID identifies the assembly.
- Placement ID identifies a location in the assembly.
- Sheet ID identifies the durable authored object.
- Revision ID identifies the Sheet state used by a compile or historical record.

## Ordering

Array order is the v0.2 candidate for solo-first human readability. Fractional order keys remain a migration option triggered by app-managed sync or concurrent manifest editing.

## Node kinds

- Sheet reference
- Container
- Generated node
- Asset reference
- Placeholder

## Inclusion resolution

Compile profile explicit override → placement inclusion → parent inheritance → Sheet default → kind default.

Excluded material remains visible, searchable, and available to alternate profiles.

## Compile significance

Roles are semantic, not styling. Titles, numbering, scene breaks, and front/back matter are resolved into a compile plan and made visible before output.

## Acceptance tests

Filesystem sorting cannot change output order. Reordering modifies the manifest but not Sheet prose. One Sheet may appear across multiple manuscripts, with shared-use visibility.
