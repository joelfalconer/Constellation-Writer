# System Overview

## Layer model

```text
AUTHORING SURFACE
Editor, navigator, inspector, command palette

        ↓ governed through

MUTATION ENVELOPE
Intent, actor, targets, base revisions, review, recovery, outcome

        ↓ commits into

CANONICAL STATE
Sheets, sidecars, manifests, profiles, entities, claims, sources

        + records into

CANONICAL EVENT HISTORY
PatchSessions, migrations, restores, conflicts, publication locks

        ↓ projected into

DERIVED MACHINERY
SQLite, FTS, graph, embeddings, previews, statistics, QA

        ↓ consumed by

RECALL, COMPILE, CONTINUITY, AND AI INSTRUMENTS
```

## Dependency law

Higher layers may depend on lower layers. Lower layers must not require higher intelligence layers to function.

- Writing must not require graph, AI, semantic retrieval, or network.
- Recovery must not require SQLite.
- Compile semantics must not depend on preview cache.
- Canonical records must not depend on embeddings or inferred graph edges.

## Initial runtime modules

- `editor`: authorship surface and local interactions.
- `vault`: canonical file I/O and project validation.
- `catalog`: rebuildable SQLite mirror and FTS.
- `manuscript`: assembly and binder projection.
- `compiler`: compile plan, transformations, QA, output, source map.
- `mutation`: governed changes and application transaction.
- `recovery`: buffers, snapshots, conflicts, archives, restore.
- `search`: literal and structural recall.
- `compendium`: minimal entity, claim, and evidence boundary.
