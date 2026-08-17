# Benchmark Dossier: Vellum

```yaml
status: refreshed_candidate
updated_at: 2026-08-17
source_basis:
  - SRC-OFFICIAL-VELLUM-SPECS-20260817
  - SRC-OFFICIAL-VELLUM-IMPORT-20260817
  - SRC-OFFICIAL-VELLUM-PRINT-20260817
evidence_unit: EU-022
epistemic_basis: source_assertion
validation_state: machine_checked_current_docs
```

## Current official product state

Vellum's current documentation establishes a publishing-oriented workflow. It imports `.docx` manuscripts, detects chapters and converts the document into Vellum's native book structure. A Navigator exposes chapters, while style and preview controls shape ebook and print presentation. Current technical specifications list EPUB ebook output, PDF/X print output, and manuscript-content export as DOCX or RTF.

Vellum's import guidance explicitly tells writers not to over-format the source Word manuscript because Vellum will ignore or clean up much appearance-level formatting. This is useful evidence that its product boundary is **publication formatting over manuscript content**, not preservation of every upstream visual choice.

## Benchmark interpretation

Vellum is a specialist benchmark for **publication confidence** rather than manuscript authorship. Its strongest transferable lesson is the separation between semantic manuscript structure, style selection, preview, and generated publication artifacts. Constellation should learn from that boundary without becoming a page-layout application.

## Atomic affordances to benchmark

- DOCX import and chapter recognition.
- Split/merge chapter cleanup after import.
- Navigator-to-preview relationship.
- Style/theme application separated from manuscript content.
- ebook and print preview confidence.
- EPUB/PDF generation and conformance checks.
- content export back to DOCX/RTF.

## Borrow / reject / test

**Borrow candidate:** publication-preview confidence, semantic style application, explicit print/ebook targets, and clear separation of manuscript content from generated layout.

**Reject candidate:** importing into an opaque publishing-native document becoming Constellation's canonical authoring model.

**Test in Constellation:** whether deterministic Workbench AST → direct Markdown/HTML → pinned publishing adapters can provide comparable confidence while preserving source maps and writer-owned canonical files.

## Evidence table

| Claim | Basis | Locator | Validation |
|---|---|---|---|
| DOCX is manuscript input; Vellum converts import into native book structure | EU-022 / SRC-OFFICIAL-VELLUM-IMPORT-20260817 | `Importing into Vellum` | machine checked |
| EPUB and print PDF are primary generated outputs; DOCX/RTF content export exists | EU-022 / SRC-OFFICIAL-VELLUM-SPECS-20260817 | `Ebook Output`, `Print Output`, `Content Export` | machine checked |
| Print preview and customization precede generation | EU-022 / SRC-OFFICIAL-VELLUM-PRINT-20260817 | `Preview and Customization` | machine checked |

## Remaining gaps

- Exact determinism and source-mapping behavior inside Vellum.
- Import/export loss on complex real manuscripts.
- Accessibility of generated artifacts versus application UI accessibility.
- Professional author switching evidence and reasons for retaining Vellum after writing elsewhere.
