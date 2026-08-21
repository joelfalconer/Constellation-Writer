# Benchmark Dossier: Scrivener

```yaml
status: refreshed_candidate
updated_at: 2026-08-17
historical_source_basis: [SRC-DR-001, EU-002]
current_source_basis:
  - SRC-OFFICIAL-SCRIVENER-BINDER-20260817
  - SRC-OFFICIAL-SCRIVENER-COMPILE-20260817
  - SRC-OFFICIAL-SCRIVENER-COMPILE-FORMATS-20260817
current_evidence_unit: EU-017
validation_state: machine_checked_current_docs
historical_locator_status: unresolved_source_unavailable
```

## Historical report finding

The inherited Deep Research ledger describes Scrivener as the strongest benchmark for project containment, Binder-scale structure, research adjacency, and compile control. The exact `SRC-DR-001` report span cannot be recovered in the current run and remains explicitly unresolved.

## Current official product state

Current Literature & Latte material establishes that:

- the **Binder** is the core project organizer for files and folders and is used to create, arrange, split, merge, and search manuscript chunks;
- writers spend most writing time in the **Editor**, while the Binder provides structural control;
- Scrivener projects support discrete scene/chapter files and folders, including structures for research and other non-Manuscript material;
- **Compile** assembles the Draft/Manuscript hierarchy into a linear output, recognizes files/folders and section types, permits inclusion/exclusion, and separates drafting appearance from output formatting;
- compile formats can be customized independently of the writing surface.

These sources establish documented mechanics. They do not establish that Scrivener is too complex, cognitively heavy, accessible, inaccessible, fast, or slow for professional users.

## Benchmark interpretation

Scrivener remains the clearest current benchmark for separating **authored chunks**, **structural hierarchy**, and **compiled output semantics**. Its strongest architectural lesson is not a visual Binder clone; it is that longform work can be assembled from discrete authored units and transformed at compile time without forcing writing-time formatting to equal publication-time formatting.

## Atomic affordances to benchmark

- Binder reorder, nesting, search, split, and merge.
- Manuscript versus research/supporting-material boundary.
- Scrivenings-style multi-document reading/editing without permanent merge.
- Compile selection, section type/layout, front/back matter, and format selection.
- Compile filters for subsets such as a POV or timeline.
- Return from structural manipulation to the active prose location.

## Borrow / reject / test

**Borrow candidate:** discrete-chunk authoring, structural organization independent of prose, adjacent research, and compile as a first-class assembly operation.

**Reject candidate:** any implementation in which the structural tree becomes the dominant mental model or the compile system owns hidden canonical semantics.

**Test in Constellation:** whether a manifest-first file model can preserve Scrivener-class structural and compile power with clearer authority boundaries, deterministic source maps, and lower recovery cost.

## Evidence table

| Claim | Basis | Locator | Validation |
|---|---|---|---|
| Historical synthesis: project container + Binder + research adjacency + compile is Scrivener's strongest contribution | EU-002 / SRC-DR-001 | unresolved: final report unavailable | unreviewed historical assertion |
| Binder is central project organizer while most writing occurs in Editor | EU-017 / SRC-OFFICIAL-SCRIVENER-BINDER-20260817 | Binder overview | machine checked |
| Compile stitches Binder elements into a linear output and supports inclusion and section-layout control | EU-017 / SRC-OFFICIAL-SCRIVENER-COMPILE-20260817 | What is compiling? / Compile Overview | machine checked |
| Compile formats are output-only settings separate from writing-time appearance | EU-017 / SRC-OFFICIAL-SCRIVENER-COMPILE-FORMATS-20260817 | What are compile formats? | machine checked |

## Remaining gaps

- Exact `SRC-DR-001` span.
- Measured long-session ergonomics, accessibility, and latency.
- Import/export loss on representative manuscripts.
- Recovery behavior for project corruption and cross-device sync conflicts.
- Current switching complaints and critical incidents from professional users.
