# F1 Architecture Coherent Readiness v0.5

## Current readiness

```yaml
status: conditional_not_ready
F0: accepted_on_main
contract_kernel: machine_checked_candidate
reference_fixture: expanded_and_machine_checked
validator: v0_2_tested_in_github_actions
negative_tests: tested_in_ci
ADR_0004_desktop_shell: accepted_Electron_for_F2_scaffold_pending_PR_merge
ADR_0005_editor_engine: proposed_pending_spike_4
ADR_0006_compile_architecture: proposed_pending_spike_5
evidence_lineage: issue_7_closure_ready_pending_refresh_PR_review_and_merge
critical_contradictions:
  - CON-003_mutation_ownership_candidate_resolution_pending_F1_confirmation
vertical_slice_6: routed_to_F2_after_F1
human_F1_review: pending
```

## Accepted baseline

F0 Project Defined remains accepted on `main`. The current F1 work is stacked deliberately: post-merge reconciliation PR #10, evidence refresh PR #11, and desktop-shell spike PR #12. None of those stacked candidate changes are described as canonical until promoted.

## F1 blocker register

| Blocker | Owner | Acceptance | Current state | Revisit trigger |
|---|---|---|---|---|
| #3 desktop shell decision | `joelfalconer` | equivalent Tauri 2/Electron controls measured; hard vetoes applied; ADR-0004 records accept/reject/defer | **closure-ready on PR #12 review/merge; Electron selected** | physical IME/accessibility veto; F2 real-hardware startup/memory budget; issue #4 shell-specific editor result |
| #4 prose editor decision | `joelfalconer` | CodeMirror 6 and a serious rival tested for longform latency, IME, bidi, accessibility, selection/undo, overlays; ADR-0005 records decision | open | before editor package architecture is accepted |
| #5 compile architecture decision | `joelfalconer` | Workbench compile plan/AST proves deterministic semantic output, source mapping, QA, and Pandoc adapter isolation; ADR-0006 records decision | open | before P2 Manuscript Machine implementation |
| #7 evidence lineage | `joelfalconer` | EU-001–010 exact locators resolved or explicitly unresolved with reason; current benchmark claims use current primary sources | closure-ready on evidence-refresh PR review/merge | if final SRC-DR-001 report becomes available or consequential benchmark claims change |
| `CON-003` mutation ownership | F1 architecture gate | Mutation Envelope remains sole transaction/application owner without PatchSession/Recovery duplication | open critical | at F1 closure; again if F2 implementation exposes competing ownership |

## Issue #3 shell result

Roadmap sequence item 3 produced equivalent Tauri and Electron shell controls using the same 50,000-word CodeMirror renderer. Final desktop workflow `32085957984` passed four matrix jobs: Windows/macOS × Electron/Tauri. Foundation contracts also remained green at the measured head in run `32085957973`.

Both controls passed bounded project-root traversal/symlink controls and retained a narrow native boundary. No automated security or rendering hard veto was observed.

ADR-0004 selects **Electron 43.2.0** for the F2 desktop scaffold because:

- the professional editor benefits unusually strongly from one bundled Chromium generation across Windows and macOS rather than two OS WebView engines;
- the single hosted-runner shell-ready result favored Electron on both measured platforms;
- the Electron control demonstrated sandboxed, context-isolated, filesystem-blind renderer operation behind a narrow bridge;
- Tauri's smaller footprint is useful but is deliberately not allowed to outrank writer-surface consistency, and the collected package/memory numbers are not sufficiently comparable to act as winner metrics.

This decision does **not** mark real IME or accessibility controls passed. VoiceOver, Narrator/NVDA, actual candidate-window input, high contrast, 200% zoom, physical file drag/drop, and representative-hardware startup/memory remain explicit veto/revisit triggers.

Evidence report: `spikes/desktop-shell/results/SHELL_SPIKE_REPORT-2026-08-18.md`.

## Issue #7 evidence result

Issue #7 remains closure-ready on PR #11 review/merge. Its historical Deep Research locator limitation remains explicit and does not silently become resolved through the technology spikes.

## F1 entry criteria

F1 entry remains valid. F1 closure is not ready.

## F1 closure criteria

F1 may close only when:

- one canonical owner exists for every modeled v1 durable field;
- foundation schemas and fixtures remain machine checked at the promotion head;
- issue #3's selected shell decision is promoted through review/merge;
- #4 and #5 produce measured evidence and ADR-0005/0006 decisions;
- issue #7 evidence refresh is merged and residual source-access limitation remains explicit;
- `CON-003` is accepted, revised, or explicitly deferred with a falsifier and no competing transaction authority;
- architectural rivals are tested or explicitly deferred with accepted risk;
- no technology choice forces hidden canonical state, source-text loss, an accepted accessibility/IME veto, or compile-adapter leakage;
- human F1 approval is recorded in a gate receipt.

## Route

1. Review and merge stacked PRs #10, #11, and #12 in order when their evidence is accepted.
2. Execute issue #4 and issue #5.
3. Integrate ADR-0005/0006 outcomes and re-run clean contract validation.
4. Run the F1 adversarial architecture closure prompt, including `CON-003`.
5. If closure passes, issue `F1_ARCHITECTURE_COHERENT_RECEIPT.md`, update state, and route directly to F2 vertical slice #6.
6. Carry shell physical IME/accessibility and real-hardware performance controls into F2/F4 as explicit veto tests rather than pretending hosted CI resolved them.
