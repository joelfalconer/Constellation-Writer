# Benchmark Dossier: iA Writer

```yaml
status: refreshed_candidate
updated_at: 2026-08-17
historical_source_basis: [SRC-DR-001, EU-003]
current_source_basis:
  - SRC-OFFICIAL-IA-FOCUS-20260817
  - SRC-OFFICIAL-IA-SYNTAX-20260817
  - SRC-OFFICIAL-IA-STYLE-20260817
  - SRC-OFFICIAL-IA-SETTINGS-20260817
current_evidence_unit: EU-018
validation_state: machine_checked_current_docs
historical_locator_status: unresolved_source_unavailable
```

## Historical report finding

The inherited Deep Research ledger treats iA Writer as the strongest editor-as-instrument benchmark, especially for syntax/style attention and provenance-oriented writing behavior. The exact `SRC-DR-001` report span remains unresolved because the final report attachment is not retrievable in this run.

## Current official product state

Current iA documentation establishes that:

- Focus Mode offers **Sentence**, **Paragraph**, and **Typewriter** scopes;
- Typewriter focus keeps the cursor vertically centered;
- Syntax Highlight marks parts of speech in the editor;
- Style Check marks fillers, redundancies, clichés, and configurable custom patterns;
- Authorship controls distinguish author categories in documents;
- these instruments are toggled from editor/settings surfaces rather than requiring a separate analysis workspace.

The documentation itself notes that Typewriter Focus may cause vertical jumping during editing and recommends disabling Focus Mode for editing when that conflict appears. That is a useful product-specific limitation, not a reason to infer general usability quality.

## Benchmark interpretation

iA Writer is a strong benchmark for **analysis that remains attached to the text surface and can be dismissed**. Its current feature set provides a concrete control for Constellation's proposed Draft/Revise distinction: sentence-level focus and text analysis are valuable only if switching them off returns to unpolluted prose.

## Atomic affordances to benchmark

- sentence/paragraph focus transitions;
- typewriter scrolling and selection interactions;
- Syntax and Style toggling latency and visual residue;
- Authorship visibility and provenance semantics;
- clean return to ordinary source presentation;
- keyboard access to analysis controls.

## Borrow / reject / test

**Borrow candidate:** editor-centered focus and analysis tools that are explicitly summonable and reversible.

**Reject candidate:** any analysis overlay that destabilizes selection, scroll, or revision work, including a Constellation equivalent of the documented Typewriter/editing jump conflict.

**Test in Constellation:** whether Draft and Revise modes can preserve source-text sovereignty while supporting overlapping comments, provenance, and patch decorations with exact restoration.

## Evidence table

| Claim | Basis | Locator | Validation |
|---|---|---|---|
| Historical synthesis: editor-as-instrument with syntax/style/provenance orientation | EU-003 / SRC-DR-001 | unresolved: final report unavailable | unreviewed historical assertion |
| Focus Mode supports Sentence, Paragraph, Typewriter | EU-018 / SRC-OFFICIAL-IA-FOCUS-20260817 | `Focus Mode` | machine checked |
| Syntax Highlight marks selectable parts of speech | EU-018 / SRC-OFFICIAL-IA-SYNTAX-20260817 | `Working With Syntax Highlight` | machine checked |
| Style Check marks language patterns and supports custom patterns | EU-018 / SRC-OFFICIAL-IA-STYLE-20260817 | `Enable Style Check` / `Custom Patterns` | machine checked |
| Settings expose Focus, Syntax, Style Check, and Authors controls | EU-018 / SRC-OFFICIAL-IA-SETTINGS-20260817 | `Advanced` | machine checked |

## Remaining gaps

- Exact `SRC-DR-001` report span.
- Measured latency and accessibility across platforms.
- Screen-reader treatment of focus/syntax/style overlays.
- Long-session fatigue evidence.
- Current professional switching complaints and praise.
