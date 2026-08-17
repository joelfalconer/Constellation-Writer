# Benchmark Dossier: Obsidian and Graph/PKM Boundary

```yaml
status: refreshed_candidate
updated_at: 2026-08-17
historical_source_basis: [SRC-DR-001, EU-005]
current_source_basis:
  - SRC-OFFICIAL-OBSIDIAN-DATA-20260817
  - SRC-OFFICIAL-OBSIDIAN-BACKLINKS-20260817
  - SRC-OFFICIAL-OBSIDIAN-GRAPH-20260817
  - SRC-OFFICIAL-OBSIDIAN-PROPERTIES-20260817
  - SRC-OFFICIAL-OBSIDIAN-PLUGINS-20260817
current_evidence_unit: EU-020
validation_state: machine_checked_current_docs
historical_locator_status: unresolved_source_unavailable
```

## Historical report finding

The inherited report-derived conclusion says graph functionality is better treated as a projection than as the primary manuscript store or writing surface. That is a normative product conclusion, not an Obsidian product fact. The exact `SRC-DR-001` span remains unresolved because the final report attachment is unavailable.

## Current official product state

Current Obsidian documentation establishes that:

- notes are Markdown-formatted plain-text files stored in a local filesystem **vault**;
- the vault can be opened and edited with other text editors and file managers;
- Obsidian maintains a local **metadata cache** to power features including Graph and Outline, and that cache can be rebuilt;
- Backlinks derive linked and unlinked mentions from notes;
- Graph view visualizes note relationships created by internal links;
- Properties are structured data stored as YAML at the top of Markdown files;
- community plugins can extend workflows and run third-party code, with explicit security warnings.

This provides direct evidence for a file-owned canonical layer plus derived relational/indexing behavior. It does not itself prove that graph navigation is inappropriate for manuscripts or that a plugin ecosystem is undesirable for every writer.

## Benchmark interpretation

Obsidian is a high-value architectural boundary case. Its current documentation demonstrates that **local plain-text files can remain primary while metadata caches, backlinks, graph views, and plugins add higher-order behavior**. For Constellation, the graph-as-projection recommendation remains a design decision supported by product doctrine and architecture tests, not something the Obsidian source can prove on its own.

## Atomic affordances to benchmark

- external file edits and live vault refresh;
- rebuildable metadata cache behavior;
- internal links, backlinks, unlinked mentions;
- YAML properties and their visible/source modes;
- graph/local-graph invocation and navigation;
- plugin installation, permission/security posture, and failure isolation.

## Borrow / reject / test

**Borrow candidate:** inspectable local files, rebuildable metadata, backlinks as a derived recall instrument, and extension boundaries that do not redefine file truth.

**Reject candidate:** making graph navigation or third-party plugins prerequisites for foundational manuscript behavior.

**Test in Constellation:** whether literal/structural search, backlinks, and optional graph projections can be fully rebuilt from canonical files while the editor and manuscript machine remain usable with all derived state deleted.

## Evidence table

| Claim | Basis | Locator | Validation |
|---|---|---|---|
| Historical normative conclusion: graph should be projection rather than manuscript truth/surface | EU-005 / SRC-DR-001 | unresolved: final report unavailable | unreviewed historical assertion |
| Notes are local Markdown plain-text files; metadata cache is rebuildable and powers graph/outline | EU-020 / SRC-OFFICIAL-OBSIDIAN-DATA-20260817 | `How Obsidian stores data` / `Metadata cache` | machine checked |
| Backlinks expose linked and unlinked mentions | EU-020 / SRC-OFFICIAL-OBSIDIAN-BACKLINKS-20260817 | `Backlinks` | machine checked |
| Graph view visualizes internal-link relationships | EU-020 / SRC-OFFICIAL-OBSIDIAN-GRAPH-20260817 | `Graph view` | machine checked |
| Properties are structured YAML data in Markdown files | EU-020 / SRC-OFFICIAL-OBSIDIAN-PROPERTIES-20260817 | `Property format` | machine checked |
| Community plugins execute third-party code and extend workflows | EU-020 / SRC-OFFICIAL-OBSIDIAN-PLUGINS-20260817 | `Community plugins` | machine checked |

## Remaining gaps

- Exact `SRC-DR-001` report span.
- Professional manuscript workflows using Obsidian without plugin-heavy customization.
- Accessibility and performance under large writing vaults.
- Sync conflict and recovery observations beyond documentation.
- Current switching motives between Obsidian and manuscript-centered tools.
