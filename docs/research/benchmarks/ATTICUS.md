# Benchmark Dossier: Atticus

```yaml
status: refreshed_candidate
updated_at: 2026-08-17
source_basis:
  - SRC-OFFICIAL-ATTICUS-QUICKSTART-20260817
  - SRC-OFFICIAL-ATTICUS-FORMATTING-20260817
  - SRC-OFFICIAL-ATTICUS-DOCX-20260817
  - SRC-OFFICIAL-ATTICUS-CHAPTER-EXPORT-20260817
evidence_unit: EU-023
epistemic_basis: source_assertion
validation_state: machine_checked_current_docs
```

## Current official product state

Atticus' current documentation presents an authoring-to-formatting workflow with a **Writing** tab and a separate **Formatting** tab. Writers can compose directly in Atticus and organize chapters, then use themes and a previewer to format the book. Publish-ready outputs include EPUB and PDF. A DOCX export preserves content and chapter titles but not the richer Atticus design layer.

The quick-start documentation says Atticus auto-saves work to its cloud service and offers a downloadable JSON snapshot for account restoration. Current support documentation also states that exporting a single chapter is not a native workflow and requires a workaround.

## Benchmark interpretation

Atticus is valuable as a boundary case for collapsing **writing + book formatting + publication export** into one product. It also exposes a direct tension with Constellation's local-first doctrine: convenient account/cloud persistence and proprietary formatting semantics can make the integrated experience smoother while weakening the principle that durable project truth remains inspectable without the service.

## Atomic affordances to benchmark

- Writing-tab chapter creation and reorganization.
- transition from writing to formatting without source duplication;
- theme application and preview;
- EPUB/PDF generation;
- basic-content DOCX round-trip;
- account/cloud autosave and JSON backup semantics;
- excerpt/single-chapter export limitations.

## Borrow / reject / test

**Borrow candidate:** a comprehensible handoff from manuscript writing to publication formatting and fast preview of output themes.

**Reject candidate:** cloud/account state as the only durable project truth or a publishing design layer that cannot be reconstructed from writer-owned files.

**Test in Constellation:** whether local canonical files plus deterministic compile profiles can provide similarly short writer-to-publication paths without losing local ownership, exact inclusion control, or recoverability.

## Evidence table

| Claim | Basis | Locator | Validation |
|---|---|---|---|
| Writing and Formatting are distinct in-product surfaces | EU-023 / SRC-OFFICIAL-ATTICUS-FORMATTING-20260817 | `How to Format Your Book with Atticus` | machine checked |
| EPUB/PDF are publication outputs; DOCX is a basic-content/editing/backup export | EU-023 / SRC-OFFICIAL-ATTICUS-QUICKSTART-20260817 + SRC-OFFICIAL-ATTICUS-DOCX-20260817 | export sections | machine checked |
| Autosave is cloud-backed and a JSON snapshot can restore account state | EU-023 / SRC-OFFICIAL-ATTICUS-QUICKSTART-20260817 | `Additional Backup & Export Options` | machine checked |
| Single-chapter export is not native and requires a workaround | EU-023 / SRC-OFFICIAL-ATTICUS-CHAPTER-EXPORT-20260817 | full article | machine checked |

## Remaining gaps

- Offline behavior and exact durability guarantees.
- Import/export loss and round-trip behavior for complex books.
- Collaboration semantics and privacy model.
- Accessibility and professional long-session writing performance.
- Current switching evidence between Atticus, Word, Scrivener, and Vellum.
