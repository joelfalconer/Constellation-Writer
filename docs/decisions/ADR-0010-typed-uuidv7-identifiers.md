# ADR-0010: Use typed UUIDv7 identifiers

- Status: proposed
- Decision class: extreme reversal cost after persistent user data
- Review gate: F1 before prototype data

## Decision

Use lowercase RFC-style UUIDv7 values with domain prefixes such as:

```text
sh_018f0000-0000-7000-8000-000000000001
ms_018f0000-0000-7000-8000-000000000001
```

The prefix communicates object type. The UUID remains opaque domain identity. Titles, paths, headings, and placement never participate in identity.

## Rationale

- Standard UUID representation and broad implementation support.
- Time ordering assists diagnostics and index locality without becoming chronology semantics.
- Prefixes reduce wrong-object mistakes in files and logs.
- Existing candidate fixtures and schemas already exercise the form.

## Constraints

- IDs are generated once and never reused.
- Sorting by ID is not manuscript order.
- Imported external IDs are preserved as provenance, not adopted unless trusted and valid.
- Prefix changes require migration and alias handling.

## Falsifier

Reject before public data if cross-language UUIDv7 support, collision guarantees, or prefix ergonomics fail implementation review.
