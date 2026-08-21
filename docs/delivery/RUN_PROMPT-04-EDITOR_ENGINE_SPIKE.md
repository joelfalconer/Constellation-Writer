# Run Prompt 04: Professional Prose Editor Engine Spike

## Shared Execution Header

You are operating on `joelfalconer/Constellation-Writer`, whose `main` branch is the canonical project source of truth.

Before changing anything:
1. Read `README.md`, `CURRENT_STATE.yaml`, `ROADMAP.md`, `PROJECT_MANIFEST.yaml`.
2. Read `docs/constitution/PRODUCT_CONSTITUTION.md`, `CANONICALITY_MATRIX.yaml`, `STATE_AUTHORITY_MATRIX.yaml`, `INVARIANT_REGISTRY.yaml`, `DEPENDENCY_RULES.md`, and relevant ADRs.
3. Read the relevant specification(s), schemas, fixtures, validation contracts, issue body, and prior receipts.
4. Inspect current GitHub issues, PRs, CI state, and branch state instead of trusting stale prose.

Operating laws:
- The editor remains the sovereign authorship surface.
- Writer-owned files/manifests hold durable truth; derived stores must remain rebuildable.
- Never introduce SQLite-only durable state.
- Identity is independent of title/path/placement.
- Mutation Envelope owns transaction/application semantics; PatchSession owns review/provenance decisions.
- No AI or automation silently mutates canonical state.
- Preserve exact failures, minority findings, rejected alternatives, and unresolved risks.
- Use deterministic code/tests for parsing, hashing, validation, performance measurement, and reproducible transforms.
- Do not promote a technology or gate because the implementation is convenient or the documentation is persuasive.

Working method:
- Treat this as a Research OS `system_design_strategy` or `computational_analysis` run as appropriate.
- Establish a compact run contract in the run receipt.
- Prefer primary/official technical documentation when current external facts matter.
- Create a dedicated branch.
- Build the smallest executable artifact that can falsify the candidate decision.
- Add fixtures and negative controls before claiming success.
- Run tests and CI.
- Update ADRs/contracts only to the extent supported by evidence.
- Open a focused PR with measured results, unresolved risks, rollback path, and gate destination.
- Do not merge your own PR unless explicitly instructed.

## Work Order: Professional prose editor decision spike (#4)

TASK: Execute issue #4 and decide ADR-0005 through measured CodeMirror 6 evidence against a serious ProseMirror control.

Build equivalent bounded renderer controls. Do not build the production editor package yet.

Both controls must use the same deterministic 50,000-word longform fixture and expose comparable operations for:
- Markdown/prose editing;
- standard, narrow, wide, and review measures where the harness permits;
- Draft and Revise modes;
- typewriter positioning;
- overlapping comment/patch decorations;
- return-token capture and restoration;
- selection, cursor, undo/redo and source extraction;
- mixed-script/bidi fixture text.

Test and record, at minimum:
- p95 synthetic keystroke-to-frame, cursor, selection and pane-toggle observations;
- exact source preservation and source-normalization pressure;
- undo round trip;
- decoration removal returning to clean source presentation;
- return-token restoration without material scroll displacement;
- synthetic composition event survival, explicitly not treated as real IME proof;
- DOM accessibility semantics, explicitly not treated as screen-reader proof;
- forced-colors/reduced-motion emulation;
- Windows and macOS renderer runs where CI permits;
- the unexecuted physical six-hour, IME, bidi, accessibility, native clipboard and drag/drop assays as explicit veto conditions.

Decision method:
- Apply hard vetoes first: source-text loss in the selected canonical model, broken undo/selection, inaccessible core editing, destructive composition behavior, or sustained unacceptable input latency.
- Compare surviving options on source sovereignty, writer feel, selection/undo correctness, overlay behavior, accessibility risk, long-document performance, implementation complexity, and reversal cost.
- Do not reward CodeMirror merely because it already fits plain text or ProseMirror merely because its document model is richer.
- Preserve a serious rival and all unmeasured physical vetoes.

Deliverables:
- bounded CodeMirror 6 and ProseMirror controls;
- deterministic 50k and source-fidelity fixtures;
- repeatable Windows/macOS benchmark workflow and raw artifacts;
- physical six-hour/IME/accessibility/native-interaction protocol;
- platform/evidence limitation log;
- ADR-0005 updated to accepted/rejected/deferred with evidence;
- editor scaffold recommendation;
- PR linked to #4.

## Run Contract

```yaml
run_id: CW-F1-EDITOR-SPIKE-004
profile: computational_analysis
project_descriptor: choose the professional prose editor engine for the local-first writing workbench
primary_outcomes:
  - falsifiable CodeMirror 6 and ProseMirror controls sharing one longform fixture
  - cross-platform renderer measurements and source-fidelity evidence
  - evidence-based ADR-0005 decision or explicit defer state
research_corpus:
  - issue_4
  - ADR_0005
  - typography_modes_navigation_accessibility_and_performance_contracts
  - current_official_CodeMirror_and_ProseMirror_documentation
constraints:
  - canonical_manuscript_remains_plain_text
  - no_block_editor_product_pivot
  - editor_transactions_do_not_own_domain_mutation_authority
  - synthetic_composition_and_ARIA_checks_must_not_be_promoted_to_physical_IME_or_screen_reader_evidence
acceptance_tests:
  - both_engines_build_and_run_in_the_same_Chromium_harness_on_windows_and_macos_or_record_exact_failure
  - CodeMirror_preserves_exact_source_at_mount_and_across_revision_overlay_toggle
  - undo_round_trip_and_return_token_controls_pass
  - p95_observations_are_recorded_without_overclaiming_hosted_runner_SLOs
  - physical_six_hour_IME_accessibility_and_native_interaction_gaps_remain_explicit
route: F1_architecture_coherent
```
