# F1 Architecture Coherent Readiness v0.6

## Current readiness

```yaml
status: conditional_not_ready
F0: accepted_on_main
F1_reconciliation: PR_10_merged
benchmark_evidence_refresh: PR_11_merged_issue_7_closed
desktop_shell: ADR_0004_Electron_accepted_issue_3_closed
editor_engine: ADR_0005_CodeMirror_6_decision_candidate_PR_13_open
compile_architecture: ADR_0006_proposed_pending_spike_5
critical_contradictions:
  - CON-003_mutation_ownership_candidate_resolution_pending_F1_confirmation
vertical_slice_6: routed_to_F2_after_F1
human_F1_review: pending
```

## Accepted baseline

The prior F1 stack has now been promoted to canonical `main` through merge `bc422e5bf0b6e5e668c3cead1f82e9b8c269a99c`. This includes post-merge reconciliation, the issue #7 evidence refresh, and the issue #3 desktop-shell decision. Issue #3 and issue #7 are closed.

The current noncanonical candidate is PR #13 for issue #4.

## F1 blocker register

| Blocker | Acceptance | Current state | Revisit trigger |
|---|---|---|---|
| #3 desktop shell | equivalent Tauri/Electron controls, hard veto review, ADR decision | **closed; Electron selected** | physical IME/accessibility, F2 real-hardware budget, editor-specific shell result |
| #4 prose editor | CodeMirror 6 + serious rival, longform/source/undo/selection/overlay evidence, ADR decision | **closure-ready on PR #13 review/merge; CodeMirror 6 selected** | physical IME/accessibility/bidi, representative hardware, six-hour writer assay |
| #5 compile architecture | Workbench plan/AST proves deterministic semantic output, source mapping, QA, Pandoc isolation | open | before Manuscript Machine implementation |
| #7 evidence lineage | historical gaps explicit; current benchmark claims use primary sources | **closed** | final SRC-DR-001 becomes available or consequential benchmark claim changes |
| `CON-003` mutation ownership | Mutation Envelope remains sole application/transaction owner | open critical | F1 closure and any F2 competing ownership evidence |

## Issue #4 editor result

Sequence item 4 built bounded CodeMirror 6 and ProseMirror controls against the same deterministic 50,446-word fixture in one Chromium harness. Decision workflow `32460827533` passed on both Windows and macOS. Foundation validation at the measured head passed in `32460827551`.

Both controls passed bounded undo round trips, non-destructive revision-overlay toggles, return-token restoration with 0 px scroll drift, synthetic composition dispatch, and DOM textbox semantics.

The hosted p95 timing results were close enough that there is no credible synthetic-performance winner. Windows cursor/selection observations were about 18 ms for both. macOS cursor/selection observations were about 33-35 ms for both, slightly above the current 32 ms target and therefore retained as a representative-hardware replication trigger rather than a candidate-specific veto.

The architectural discriminator was source sovereignty. CodeMirror preserved the canonical source string directly. The ProseMirror Markdown parser/serializer failed the dedicated source-fidelity fixture's exact round trip, demonstrating normalization pressure at the structured-document conversion boundary.

ADR-0005 therefore selects **CodeMirror 6 for the F2 professional prose editor scaffold**, with ProseMirror retained as the serious structured-editor rival.

This decision does **not** mark physical IME, screen-reader, bidi caret/selection, native interaction, high-contrast/200% zoom, or six-hour writer controls passed. Those remain explicit veto/revisit work through the manual protocol.

Evidence:

- report: `spikes/editor-engine/results/EDITOR_ENGINE_SPIKE_REPORT-2026-08-21.md`
- Windows artifact `9438891488`, `sha256:68daf976fe6e08d264f071173a3e064d1fe0e1a52afdca666c36345eec5363e8`
- macOS artifact `9438883335`, `sha256:a7fe1cddc5357ea9c0286d270b5ce917cb75ec441d1883e8dcb2fcc95a8fef0c`

## Preserved spike failures

Two Windows harness failures preceded the green decision run: `32460543378` and `32460687987` both failed with Node 24 `spawn EINVAL` while launching the Vite preview process. The final harness launches Vite through the Node executable and an absolute `vite.js` path. These failures are recorded as cross-platform harness friction, not editor-engine evidence.

## F1 entry and closure

F1 entry remains valid. F1 closure is not ready.

F1 may close only when:

- one canonical owner exists for every modeled v1 durable field;
- foundation schemas and fixtures remain machine checked at the promotion head;
- PR #13 is reviewed/merged if its editor decision is accepted;
- issue #5 produces measured evidence and an ADR-0006 decision;
- `CON-003` is accepted, revised, or explicitly deferred with a falsifier and no competing application authority;
- architectural rivals remain preserved or explicitly retired with accepted evidence;
- no selected technology forces hidden canonical state, source-text loss, an accepted physical accessibility/IME veto, or compile-adapter leakage;
- adversarial F1 closure passes;
- human F1 approval is recorded in the gate receipt.

## Route

1. Review PR #13 and promote the issue #4 decision if accepted.
2. Execute issue #5 compile architecture spike.
3. Integrate ADR-0006 and run clean contract validation.
4. Run the F1 adversarial architecture closure prompt, explicitly adjudicating `CON-003` and the remaining physical-veto carry-forwards.
5. If closure passes, issue `F1_ARCHITECTURE_COHERENT_RECEIPT.md`, update state, and route directly to F2 vertical slice #6.
6. Carry physical shell/editor IME, accessibility, bidi, native-interaction, six-hour writer, and representative-hardware performance controls into executable product validation without pretending hosted CI already resolved them.
