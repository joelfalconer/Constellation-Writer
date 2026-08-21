# Run Receipt: CW-F1-EDITOR-SPIKE-004

## Run contract

```yaml
run_id: CW-F1-EDITOR-SPIKE-004
profile: computational_analysis
project_descriptor: choose the professional prose editor engine for Constellation Writer
primary_outcomes:
  - falsifiable CodeMirror 6 and ProseMirror controls sharing one longform fixture
  - Windows and macOS source/undo/selection/overlay/performance evidence
  - ADR-0005 decision or explicit defer state
constraints:
  - canonical manuscript remains exact plain text
  - no block-editor product pivot
  - editor transactions do not own domain mutation authority
  - synthetic composition and DOM semantics are not physical IME or screen-reader proof
route: F1_architecture_coherent
```

## Research OS runtime

Research OS v0.4.1 was loaded for this consequential run:

- Tier 0: pipeline, profiles, methods;
- Tier 1: records, controls, context lineage, criteria.

The selected profile was `computational_analysis`: deterministic scripts own fixture generation, measurement, validation, and reproducible transforms; model reasoning owns interpretation, candidate comparison, and governance.

Hard gates were applied before comparative preference. The structured-editor rival and all unmeasured physical vetoes remain visible.

## Source versions / corpus

- GitHub issue #4, `Spike: CodeMirror 6 as a professional prose editor`.
- ADR-0005 proposed CodeMirror candidate as inherited from canonical main.
- `docs/product/TYPOGRAPHY.md`.
- `docs/product/MODES.md`.
- `docs/product/NAVIGATION_RETURN.md`.
- `docs/product/ACCESSIBILITY.md`.
- `docs/product/ERGONOMICS.md`.
- `docs/validation/PERFORMANCE_BUDGET.yaml`.
- official CodeMirror and ProseMirror documentation registered in `spikes/editor-engine/OFFICIAL_SOURCE_NOTES.md`.
- successful measurement artifacts from workflow `32460827533`.

### Context omission / degraded provenance

`docs/delivery/ROADMAP_EXECUTION_PROMPTS.md`, named by the operator as the work-order source, was not present in the repository tree available to this run. The Shared Execution Header was recovered exactly from the already-preserved Run Prompt 03. Sequence Item 4 scope was grounded in issue #4, ADR-0005, and the current product/validation contracts. No missing work-order wording was fabricated.

Recovery path: if the original roadmap prompt source reappears, compare it against `RUN_PROMPT-04-EDITOR_ENGINE_SPIKE.md` and issue a delta if the omitted text changes the acceptance contract.

## Method invocations

1. **Preflight / run contract**: bounded decision, hard vetoes, acceptance tests, route, and non-goals.
2. **Deterministic fixture generation**: one reproducible 50,446-word mixed-script fixture plus source-fidelity fixture.
3. **Rival implementation**: CodeMirror 6 raw-source control and ProseMirror Markdown parse/serialize control under one Vite/Chromium harness.
4. **Negative/hard-gate controls**: exact source, overlay non-mutation, undo round trip, return-token scroll drift, finite measurements.
5. **Cross-platform measurement**: Windows/macOS hosted Chromium p95 synthetic frame observations.
6. **Failure diagnosis**: preserved two Windows preview-spawn failures and repaired the harness portably.
7. **Candidate evaluation**: hard gates first; source sovereignty, latency, overlay behavior, implementation cost, risk, and reversal cost second.
8. **Governed closure**: ADR decision candidate, report, manual physical-veto protocol, F1 route, and rollback triggers.

## Produced artifacts

- `docs/delivery/RUN_PROMPT-04-EDITOR_ENGINE_SPIKE.md`
- `spikes/editor-engine/` CodeMirror and ProseMirror controls
- `.github/workflows/editor-engine-spike.yml`
- `spikes/editor-engine/MANUAL_PROTOCOL.md`
- `spikes/editor-engine/LIMITATIONS.md`
- `spikes/editor-engine/results/RESULTS_SUMMARY.yaml`
- `spikes/editor-engine/results/EDITOR_ENGINE_SPIKE_REPORT-2026-08-21.md`
- updated ADR-0005, decision ledger, current state, and F1 readiness report

## Measurements

Decision head: `fbe91cf91ae5122887768d8469a99d744277fb6d`.

Editor workflow `32460827533`: **success** on Windows and macOS.  
Foundation workflow `32460827551`: **success**.

Artifacts:

- Windows `9438891488`, `sha256:68daf976fe6e08d264f071173a3e064d1fe0e1a52afdca666c36345eec5363e8`
- macOS `9438883335`, `sha256:a7fe1cddc5357ea9c0286d270b5ce917cb75ec441d1883e8dcb2fcc95a8fef0c`

CodeMirror p95 observations:

- Windows: keystroke 17.6 ms, cursor 18.2 ms, selection 18.2 ms, pane 17.5 ms;
- macOS: keystroke 19.9 ms, cursor 33.5 ms, selection 33.1 ms, pane 20.5 ms.

ProseMirror p95 observations:

- Windows: keystroke 17.5 ms, cursor 18.0 ms, selection 18.0 ms, pane 17.6 ms;
- macOS: keystroke 20.6 ms, cursor 34.8 ms, selection 33.3 ms, pane 18.4 ms.

The timing frontier is effectively tied in this harness. The macOS cursor/selection observations are retained as a shared replication warning because both candidates slightly exceeded the current 32 ms maximum target.

## Source-fidelity result

- CodeMirror canonical raw source exact at mount: **pass**.
- CodeMirror revision overlay removal preserves source: **pass**.
- CodeMirror undo round trip: **pass**.
- CodeMirror return-token scroll drift: **0 px**.
- ProseMirror longform generated fixture round trip: pass.
- ProseMirror dedicated source-fidelity fixture exact round trip: **fail**.

The ProseMirror result is not interpreted as a general quality failure. It is evidence that a structured Markdown parse/serialize boundary can normalize exact source representation, which conflicts with this project's stronger plain-text canonicality rule.

## Preserved failures

- `32460543378`, Windows: Node 24 `spawn EINVAL` launching Vite preview.
- `32460687987`, Windows: same failure after the first path conversion repair.
- Final repair: launch Vite through `process.execPath` plus absolute `vite.js`; run `32460827533` passed both platforms.

These failures are harness portability evidence, not candidate vetoes.

## Epistemic annotation

- CI build/test outcomes: `epistemic_basis: measurement`, `validation_state: tested`.
- p95 hosted frame observations: `epistemic_basis: measurement`, `validation_state: tested_on_hosted_runner_only`.
- ProseMirror source normalization: `epistemic_basis: measurement`, `validation_state: replicated_on_windows_and_macos`.
- CodeMirror selection: `epistemic_basis: derived_result`, `work_function: decision`, `validation_state: candidate_pending_PR_promotion`.
- Physical IME/accessibility/bidi/six-hour behavior: `validation_state: unreviewed`, deliberately unresolved.

## Decision

ADR-0005 selects **CodeMirror 6 as the F2 professional prose editor scaffold**. ProseMirror remains the serious fallback/rival.

The decisive factor is not a synthetic latency victory. Both candidates were close. CodeMirror wins because it preserves the exact canonical source directly while satisfying the bounded revision/undo/return controls, whereas the ProseMirror structured-document boundary demonstrated source-normalization pressure under the dedicated fixture.

## Unresolved items

No claim is made that hosted CI validates:

- real IME candidate windows or conversion;
- VoiceOver, Narrator, or NVDA;
- real bidi caret and selection behavior;
- physical high contrast or 200% zoom usability;
- native clipboard/drag, dead keys, key repeat, or platform text services;
- six-hour professional writing comfort;
- representative-hardware latency/resource budgets.

The manual protocol routes those as explicit physical veto/revisit controls.

## Destination

- PR #13 review and merge closes issue #4 if the decision is accepted.
- F1 remains open for issue #5, `CON-003`, adversarial closure, promotion validation, and human approval.
- F2/F4 inherit the physical editor veto suite and representative-hardware performance replication.

## Review / invalidation triggers

Reopen ADR-0005 if CodeMirror fails physical IME, assistive technology, bidi caret/selection, native interaction, accepted latency budgets, or six-hour writer controls. Any editor-engine reversal must replace the adapter/derived editor state without migrating canonical writer-owned source or moving durable authority into the editor model.
