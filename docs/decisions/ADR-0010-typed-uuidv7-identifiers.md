# ADR-0010: Use typed UUIDv7 identifiers

- Status: accepted
- Decision class: extreme reversal cost after persistent user data
- Review gate: F1 before prototype data
- Accepted at: F1 architecture-coherence adversarial closure

## Decision

Use lowercase RFC-style UUIDv7 values with domain prefixes such as:

```text
sh_018f0000-0000-7000-8000-000000000001
ms_018f0000-0000-7000-8000-000000000001
```

The prefix communicates object type. The UUID remains opaque domain identity. Titles, paths, headings, timestamps, and placement never participate in identity.

## Rationale

- Standard UUID representation and broad implementation support.
- Time ordering assists diagnostics and index locality without becoming chronology semantics.
- Prefixes reduce wrong-object mistakes in files and logs.
- Existing candidate fixtures and schemas already exercise the form.
- It preserves the core identity invariant while avoiding a proprietary identifier format.

## Serious rivals considered

### Untyped UUIDv7

Viable, but weaker for human inspection and cross-object validation. The prefix is a cheap domain guard while the UUID remains the actual opaque identity.

### ULID

Rejected for the canonical v1 identity. It provides sortable opaque IDs but would create a second non-UUID identity convention without enough product value to justify the divergence.

### UUIDv4

Viable but loses useful monotonic/index-locality characteristics available from UUIDv7 without adding meaningful architectural simplicity.

### Path/title-derived identity

Rejected by hard invariant. Rename, move, title change, or manuscript placement must never alter object identity.

## Constraints

- IDs are generated once and never reused.
- Sorting by ID is not manuscript order, creation-order semantics, or user-visible chronology.
- Imported external IDs are preserved as provenance, not adopted unless trusted, validated, and explicitly mapped.
- Prefixes are validated against object type.
- Prefix changes require migration and alias handling.
- UUIDv7 generation must use a conforming implementation and must not depend on application wall-clock ordering for correctness.

## Falsifier

Reopen before durable user data if cross-language UUIDv7 support, collision guarantees, parser ergonomics, or prefix handling fail implementation review. After durable user data exists, any change requires an explicit migration and alias strategy.

## F2 checks

- generate and parse IDs consistently in all implementation languages used by the substrate;
- reject wrong-type prefixes at schema/application boundaries;
- prove rename, move, reorder, duplicate-file detection, archive/restore, and cache rebuild preserve identity;
- verify clock irregularity does not create correctness dependence on UUID ordering;
- ensure no UI or compile path accidentally treats lexicographic ID order as manuscript order.
