# Dependency Direction Rules

## Layer order

```text
shared contracts
  → canonical file models
    → mutation and recovery substrate
      → derived catalog and indexes
        → editor, binder, search, compile, continuity instruments
          → optional AI and transmedia systems
```

## Hard rules

- Canonical files must not depend on SQLite rows to be interpreted.
- The editor may use derived indexes but must open and save Sheets without them.
- Compile may use caches for speed but must resolve from frozen canonical inputs.
- Compendium projections may depend on claims and evidence; claims may not depend on graph projection.
- AI features may consume context packs; core writing may not depend on AI availability.
- Recovery may inspect mutation history; current project validity may not depend on retaining every low-value session event.
- Package dependencies must follow the layer order or record an approved exception.

## Forbidden cycles

- editor ↔ compendium canonical mutation cycle
- compile ↔ UI state
- vault ↔ derived search index as authority
- PatchSession ↔ Recovery as competing transaction owners
- graph projection ↔ claim canonicality

## Enforcement

The validator should eventually inspect package manifests and architecture metadata for prohibited dependencies. Until code exists, ADR and PR review enforce these rules.
