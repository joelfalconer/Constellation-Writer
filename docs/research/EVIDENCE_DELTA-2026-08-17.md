# Evidence Delta Report — Issue #7

**Run date:** 2026-08-17  
**Profile:** Research OS `source_audit` + `update_delta`, with deterministic ledger maintenance  
**Sequence item:** 2 — Evidence lineage and benchmark refresh

## Run Contract

```yaml
project_descriptor: Constellation Writer F1 evidence-lineage refresh
decision_context: determine whether issue_7 evidence requirements are closure-ready without promoting inference or fabricating historical locators
primary_outcomes:
  - resolve EU-001..EU-010 locator state honestly
  - refresh eight benchmark products from current primary/official documentation
  - leave F1 architecture recommendations epistemically separate from product evidence
research_questions:
  - which inherited claims can be located in the historical Deep Research source?
  - which current benchmark mechanics are supported by official documentation as of 2026-08-17?
  - which prior switching/friction statements must remain hypotheses?
research_corpus:
  - repository research ledgers and benchmark dossiers
  - SRC-DR-001 registry reference
  - targeted File Library search for the final Deep Research report
  - official vendor documentation for eight benchmark products
constraints:
  - no model-memory backfill of missing report spans
  - no vendor documentation treated as user sentiment
  - EU-011+ remain inference/design unless independently evidenced
  - no architecture promotion from product-feature presence alone
non_goals:
  - user interviews
  - long-session usability testing
  - accessibility certification
  - performance measurement
  - technology ADR closure
acceptance_tests:
  - no EU-001..EU-010 locator remains pending_exact_span
  - unresolved historical locators carry explicit reason
  - every consequential current benchmark claim has a registered official locator
  - all eight requested product dossiers have current-state evidence
  - switching and friction hypotheses remain visibly non-evidentiary
  - repository validation remains clean
destination: focused PR linked to issue_7 and F1 gate
```

## Executive result

The refresh **improves evidence integrity without pretending the historical report locator gap disappeared**.

The final `SRC-DR-001` Deep Research report could not be retrieved from the repository or targeted File Library searches. Those searches returned precursor research briefs and prompts, which are useful method lineage but cannot prove the final findings. EU-001 through EU-010 therefore now use `unresolved_source_unavailable` with a precise reason instead of the non-informative `pending_exact_span` placeholder.

At the same time, current official documentation was collected for all eight required benchmark products. New evidence units EU-016 through EU-023 establish current documented mechanics while keeping them separate from the inherited historical synthesis and from Constellation architecture recommendations.

## Evidence delta

| Area | Before | After |
|---|---|---|
| EU-001–EU-010 | `pending_exact_span` | explicit `unresolved_source_unavailable` reason; current corroboration linked where appropriate |
| EU-011+ | conversation-derived inference/design | unchanged epistemic class; no promotion by repetition |
| Ulysses | one historical inherited assertion | current Sheets/Groups, Export, External Folders, Goals sources + EU-016 |
| Scrivener | one historical inherited assertion | current Binder and 2025–2026 Compile sources + EU-017 |
| iA Writer | one historical inherited assertion | current Focus/Syntax/Style/settings sources + EU-018 |
| Drafts | one historical inherited assertion | current Getting Started/Actions/Workspaces/Tags + EU-019 |
| Obsidian | historical architecture-oriented assertion | current local Markdown/cache/backlinks/graph/properties/plugins + EU-020 |
| Final Draft | evidence-gap placeholder | current product dossier + EU-021 |
| Vellum | evidence-gap placeholder | current product dossier + EU-022 |
| Atticus | evidence-gap placeholder | current product dossier + EU-023 |
| switching map | candidate synthesis could be read as observed behavior | explicitly hypothesis-only; current mechanics linked but no migration motive invented |
| friction map | design responses with sparse evidence boundary | current mechanic references separated from untested friction hypotheses |

## Current source findings relevant to F1

### Ulysses

Current official documentation confirms a Sheet/Group writing model, multi-item export, goals at several scopes, and External Folder interoperability. It also documents capability differences between interoperable Markdown files and native Ulysses files. This is evidence for a real product tradeoff, not proof that either storage choice is superior for Constellation.

### Scrivener

Current official material confirms the Binder as the structural project organizer, discrete writing chunks, and Compile as an assembly/transform layer whose formatting can differ from the writing surface. This directly strengthens the benchmark basis for issue #5 without proving Constellation's proposed compiler architecture.

### iA Writer

Current official support documents editor-centered Focus, Syntax, Style, and Authorship controls. Focus Mode documentation also names an editing interaction in which Typewriter mode may produce vertical jumping, a useful reminder that a focus affordance can conflict with revision behavior.

### Drafts

Current official documentation confirms plain-text editing, a Draft List, an explicit Action List, Workspaces, and tagging. This supports the capture/routing/action-grammar benchmark while leaving performance and professional preference unmeasured.

### Obsidian

Current official documentation is unusually valuable to the architecture boundary: local Markdown files are primary, while a rebuildable metadata cache powers Graph/Outline behavior. Backlinks, Graph, YAML Properties, and plugins are documented layers over the vault. This supports the plausibility of file truth plus derived intelligence, not the normative claim that Constellation must copy Obsidian.

### Final Draft

Official material confirms screenplay-specialist structure: Beat Board story units can feed a page-aware Outline Editor and then script pages; FDX is the standard Final Draft document format. This strengthens the case for keeping screenplay semantics in a specialist dialect/adapter boundary rather than universalizing them prematurely.

### Vellum

Official documentation confirms DOCX manuscript import, conversion to a Vellum-native book, chapter navigation, styling/preview, EPUB/print PDF generation, and DOCX/RTF content export. This makes Vellum a strong publication-forge benchmark but does not establish deterministic internals or round-trip fidelity.

### Atticus

Official documentation confirms distinct Writing and Formatting surfaces, publish-ready EPUB/PDF output, basic-content DOCX export, cloud autosave, downloadable JSON account snapshot, and a workaround rather than native single-chapter export. This creates a concrete integrated-publishing versus local-first-authority comparison without turning that contrast into a negative product judgment.

## Claims deliberately not made

- No claim that the final Deep Research report's exact EU-001–EU-010 spans were recovered.
- No claim that any benchmark product is objectively best, calmest, fastest, most accessible, or most trustworthy.
- No claim about actual switching frequency or motives.
- No claim that vendor documentation demonstrates long-session professional value.
- No claim that current product mechanics validate Constellation's Mutation Envelope, PatchSession, recovery, compiler, editor engine, or shell decisions.

## New uncertainties

1. **UNC-EVID-001:** historical report locator recovery remains blocked until the final report attachment or archive copy becomes available.
2. **UNC-EVID-002:** official documentation now covers current mechanics well, but professional usability, fatigue, accessibility quality, and switching remain weakly evidenced.
3. **UNC-EVID-003:** Vellum/Atticus illustrate integrated publication convenience while Constellation prioritizes writer-owned durable truth; the correct implementation boundary remains an issue #5/#6 test question, not a benchmark verdict.

These are recorded in `CONTRADICTIONS.yaml` as research uncertainties rather than smoothed away.

## Artifacts changed

- `SOURCE_REGISTRY.yaml`
- `SOURCE_DECISIONS.yaml`
- `EVIDENCE_UNITS.jsonl`
- `FEATURE_ATOMICITY.yaml`
- `SWITCHING_MAP.md`
- `WORKFLOW_FRICTION_MAP.md`
- `COVERAGE_REPORT.md`
- `CONTRADICTIONS.yaml`
- refreshed Ulysses, Scrivener, iA Writer, Drafts, and Obsidian dossiers
- new Final Draft, Vellum, and Atticus dossiers
- `SOURCE_COVERAGE_MATRIX-2026-08-17.md`
- compiled execution prompt for this sequence item

## Gate assessment

**Issue #7:** closure-ready when this PR passes validation and is reviewed/merged. The issue explicitly permits historical evidence units to remain unresolved when the reason is recorded.  
**F1:** remains `conditional_not_ready`; this run does not close #3, #4, #5, or `CON-003`.

## Routing / closure

```yaml
route: F1_evidence_package
owner: joelfalconer
first_action_after_merge: remove_issue_7_from_active_F1_blockers_and_continue_to_issue_3_or_4_per_roadmap
acceptance_test: issue_7_PR_merged_with_clean_validation
review_trigger: final_SRC_DR_001_report_becomes_available_or_new_current_product_claim_added
rollback_condition: any_current_claim_lacks_official_locator_or_any_inference_is_found_promoted_as_evidence
```
