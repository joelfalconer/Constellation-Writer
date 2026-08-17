# Benchmark Dossier: Ulysses

```yaml
status: refreshed_candidate
updated_at: 2026-08-17
historical_source_basis: [SRC-DR-001, EU-001]
current_source_basis:
  - SRC-OFFICIAL-ULYSSES-SHEETS-20260817
  - SRC-OFFICIAL-ULYSSES-EXPORT-20260817
  - SRC-OFFICIAL-ULYSSES-EXTERNAL-20260817
  - SRC-OFFICIAL-ULYSSES-GOALS-20260817
current_evidence_unit: EU-016
validation_state: machine_checked_current_docs
historical_locator_status: unresolved_source_unavailable
```

## Historical report finding

The inherited Deep Research ledger characterizes Ulysses as strongest when calm writing, library organization, and export live in one restrained environment. That finding remains `EU-001`, but the final `SRC-DR-001` report attachment is not retrievable in this run, so its exact report span remains explicitly unresolved rather than guessed.

## Current official product state

Official Ulysses documentation currently establishes that:

- all writing is done in **Sheets**, stored in **Groups**;
- Sheets behave like documents without requiring a title or filename as their organizing concept;
- multiple Sheets, Groups, and filters can be exported through an export preview to HTML, ePub, PDF, DOCX, or plain text;
- goals can be attached at Sheet, Group, and Project scope;
- External Folders can expose local/cloud material through Finder and third-party applications, including Markdown files, though external Markdown loses some native Ulysses features and automatic Ulysses backups.

These are documented capabilities, not evidence that Ulysses is objectively calmer, faster, more accessible, or more trustworthy under professional fatigue.

## Benchmark interpretation

The strongest current, source-supported contribution is the coupling of a small writing unit, library-scale navigation, goals, and direct multi-item export without requiring a separate publishing application. External Folder support also creates an important boundary case: portability can be increased, but capability parity with native library storage is reduced.

## Atomic affordances to benchmark

- Sheet creation, selection, grouping, split/merge, and return cost.
- Material Sheet exclusion from export and goals/stats where applicable.
- Group/project goal visibility without dashboard dominance.
- Export selection, preview, style selection, and multi-Sheet assembly confidence.
- Native-library versus External-Folder capability differences.

## Borrow / reject / test

**Borrow candidate:** calm editor dominance, Sheet-scale authoring, library immediacy, lightweight goal attachment, and export that can assemble multiple writing units.

**Reject candidate:** making the writer choose between full product capability and inspectable local files as a permanent architectural tradeoff.

**Test in Constellation:** whether manifest-first assembly and writer-owned files can retain Ulysses-class immediacy while improving recovery, explicit export semantics, and external inspectability.

## Evidence table

| Claim | Basis | Locator | Validation |
|---|---|---|---|
| Historical synthesis: calm editor + library + export is Ulysses' strongest benchmark contribution | EU-001 / SRC-DR-001 | unresolved: final report unavailable | unreviewed historical assertion |
| Writing unit is the Sheet; Sheets are organized in Groups | EU-016 / SRC-OFFICIAL-ULYSSES-SHEETS-20260817 | `Sheets & Groups` | machine checked |
| Multi-Sheet/Group export supports preview and common output formats | EU-016 / SRC-OFFICIAL-ULYSSES-EXPORT-20260817 | `Export` | machine checked |
| Goals exist at Sheet, Group, and Project scope | EU-016 / SRC-OFFICIAL-ULYSSES-GOALS-20260817 | `Goals` | machine checked |
| External Folders permit interoperable Markdown but with reduced native capabilities | EU-016 / SRC-OFFICIAL-ULYSSES-EXTERNAL-20260817 | `External Folders` | machine checked |

## Remaining gaps

- Long-session editor ergonomics and measured latency.
- Accessibility behavior across supported Apple platforms.
- Recovery and sync-conflict behavior under destructive tests.
- Current professional switching complaints and praise.
- Exact `SRC-DR-001` report locator.
