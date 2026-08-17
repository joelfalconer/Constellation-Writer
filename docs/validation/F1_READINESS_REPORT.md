# F1 Architecture Coherent Readiness v0.4

## Current readiness

```yaml
status: conditional_not_ready
F0: accepted_on_main
contract_kernel: machine_checked_candidate
reference_fixture: expanded_and_machine_checked
validator: v0_2_tested_in_github_actions
negative_tests: tested_in_ci
technology_adrs_0004_0005_0006: proposed_pending_spikes
evidence_lineage: issue_7_closure_ready_pending_refresh_PR_review_and_merge
historical_report_locator_limit: SRC_DR_001_final_attachment_unavailable_explicitly_recorded
critical_contradictions:
  - CON-003_mutation_ownership_candidate_resolution_pending_F1_confirmation
vertical_slice_6: routed_to_F2_after_F1
human_F1_review: pending
```

## Accepted baseline

F0 Project Defined was accepted by the project owner through the instruction to merge foundation PR #1. The foundation was promoted to `main` through merge commit `1f01da3c76611d9ad9b1b297c2b8f265a91a6daa`.

A clean GitHub Actions checkout of that merge commit completed successfully in run `32010291279`. The preserved validation artifact reports validator v0.2.0 passed with 22 schemas, 3 Sheets, 2 manuscripts, and zero issues. The workflow also completed the contract negative-test suite successfully.

This establishes the machine baseline for F1 entry. It does not prove desktop, editor, compile, recovery, or writer-experience behavior.

## F1 blocker register

| Blocker | Owner | Acceptance | Current state | Revisit trigger |
|---|---|---|---|---|
| #3 desktop shell decision | `joelfalconer` | equivalent Tauri 2/Electron controls measured; hard vetoes applied; ADR-0004 records accept/reject/defer | open | before desktop application scaffold is accepted |
| #4 prose editor decision | `joelfalconer` | CodeMirror 6 and a serious rival tested for longform latency, IME, bidi, accessibility, selection/undo, overlays; ADR-0005 records decision | open | before editor package architecture is accepted |
| #5 compile architecture decision | `joelfalconer` | Workbench compile plan/AST proves deterministic semantic output, source mapping, QA, and Pandoc adapter isolation; ADR-0006 records decision | open | before P2 Manuscript Machine implementation |
| #7 evidence lineage | `joelfalconer` | EU-001–010 exact locators resolved or explicitly unresolved with reason; current benchmark claims use current primary sources | closure-ready on evidence-refresh PR review/merge | if final SRC-DR-001 report becomes available or consequential benchmark claims change |
| `CON-003` mutation ownership | F1 architecture gate | Mutation Envelope remains sole transaction/application owner without PatchSession/Recovery duplication | open critical | at F1 closure; again if F2 implementation exposes competing ownership |

## Issue #7 evidence result

The evidence-refresh run completed the gate-relevant work without manufacturing historical provenance:

- EU-001 through EU-010 no longer contain `pending_exact_span`; each now records `unresolved_source_unavailable` with the exact reason the final Deep Research report span cannot be recovered in the current run.
- Targeted File Library search found precursor research briefs but not the final report; those briefs were explicitly excluded as finding evidence.
- Current official documentation has been registered for Ulysses, Scrivener, iA Writer, Drafts, Obsidian, Final Draft, Vellum, and Atticus.
- EU-016 through EU-023 represent current documented product mechanics separately from historical report findings.
- Switching and friction maps now distinguish product mechanics from untested user-behavior hypotheses.
- `SOURCE_COVERAGE_MATRIX-2026-08-17.md` and `EVIDENCE_DELTA-2026-08-17.md` record coverage and residual uncertainty.

Because issue #7 explicitly permits an exact locator to remain unresolved when the reason is recorded, this work is closure-ready once its PR validates and is merged. The historical source-access limitation remains visible as `UNC-EVID-001`.

## F1 entry criteria

| Criterion | State |
|---|---|
| F0 acceptance recorded | pass |
| foundation merge verified on main | pass |
| clean main schema/fixture validation | pass at run `32010291279` |
| negative contract controls execute | pass through CI test suite |
| modeled authority drift check clean | pass within validator scope |
| deliverables and operational state reconciled | pass candidate in PR #10 |
| critical architecture contradictions have explicit routes | pass candidate |
| technology spike plans have falsifiable acceptance measures | pass, issues #3–#5 |
| evidence-lineage remediation | closure-ready pending evidence-refresh PR validation/merge |

**F1 entry decision: valid. F1 closure decision: not ready.**

## F1 closure criteria

F1 may close only when:

- one canonical owner exists for every modeled v1 durable field;
- foundation schemas and fixtures remain machine checked at the promotion head;
- #3, #4, and #5 produce measured evidence and ADR-0004/5/6 decisions;
- the issue #7 evidence refresh is merged and its residual source-access limitation remains explicit;
- `CON-003` is accepted, revised, or explicitly deferred with a falsifier and no competing transaction authority in the contracts;
- architectural rivals are tested or explicitly deferred with accepted risk;
- technology choices do not force hidden canonical state, source-text loss, accessibility vetoes, or compile-adapter leakage;
- human F1 approval is recorded in a gate receipt.

## Sequencing note: vertical slice #6

The accepted roadmap execution prompts place F1 closure before F2 durable substrate vertical slice #6. #6 is the first F2 execution route after F1 passes and may later falsify an F1 assumption. It is not evidence that F1 has already passed.

## Route

1. Review and merge the issue #7 evidence-refresh PR when its validation is clean.
2. Execute #3, #4, and #5, preferably in parallel where environments permit.
3. Integrate their receipts and ADR outcomes.
4. Run the F1 adversarial architecture closure prompt.
5. If closure passes, issue `F1_ARCHITECTURE_COHERENT_RECEIPT.md`, update state, and route directly to #6.
6. If closure fails, create only the targeted remediation issues required by the evidence.
