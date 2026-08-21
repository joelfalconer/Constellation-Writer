# Benchmark Dossier: Final Draft

```yaml
status: refreshed_candidate
updated_at: 2026-08-17
source_basis:
  - SRC-OFFICIAL-FINALDRAFT-OUTLINE-20260817
  - SRC-OFFICIAL-FINALDRAFT-BEATBOARD-20260817
  - SRC-OFFICIAL-FINALDRAFT-EXPORT-20260817
evidence_unit: EU-021
epistemic_basis: source_assertion
validation_state: machine_checked_current_docs
```

## Current official product state

Final Draft's official documentation currently describes a screenplay-specific planning pipeline in which writers can organize story units on a **Beat Board**, move them into the page-aware **Outline Editor**, and send outline content into script pages. The Beat Board supports ideas, notes, story points, scene fragments, scenes, sequences, acts, and longer arcs. The Outline Editor places beats on horizontal lanes tied to screenplay page ranges. Final Draft's standard document format is `.fdx`, with export paths to other formats.

## Benchmark interpretation

Final Draft is a specialist control for the question: **which structural semantics are intrinsic to screenplay production rather than generic longform writing?** Beat-to-outline-to-page continuity and page-aware structure are genuine specialist mechanics. They should not automatically infect prose Sheets or manuscript manifests.

## Atomic affordances to benchmark

- Beat creation and freeform spatial organization.
- Transfer from Beat Board to linear Outline Editor.
- Page-range sizing and scene/act planning.
- Send-to-script transition.
- Show/hide outline material while drafting.
- FDX interchange and lossy/non-lossy export boundaries.
- Revision-production semantics not yet covered in this refresh.

## Borrow / reject / test

**Borrow candidate:** script-specific structural adapter concepts and explicit transitions between planning structure and screenplay pages.

**Reject candidate:** making every Constellation manuscript page-aware or screenplay-semantic.

**Test in Constellation:** represent screenplay structure through `script` Sheets/Fountain or FDX adapters only if a bounded screenplay assay demonstrates that generic manuscript placements cannot carry the required semantics cleanly.

## Evidence table

| Claim | Basis | Locator | Validation |
|---|---|---|---|
| Beat Board supports story beats from notes/fragments through acts and series arcs | EU-021 / SRC-OFFICIAL-FINALDRAFT-BEATBOARD-20260817 | `What is the Beat Board?` | machine checked |
| Beat Board → Outline Editor → script pages is a documented workflow | EU-021 / SRC-OFFICIAL-FINALDRAFT-OUTLINE-20260817 | `How can I outline a script in Final Draft?` | machine checked |
| FDX is the standard Final Draft document format and export supports additional formats | EU-021 / SRC-OFFICIAL-FINALDRAFT-EXPORT-20260817 | export format list | machine checked |

## Remaining gaps

- Revision colors, production locking, scene numbering, collaboration, and pagination edge cases.
- Exact interchange-loss tests between Fountain, FDX, PDF, and Constellation candidates.
- Professional screenwriter workflow observation and accessibility testing.
