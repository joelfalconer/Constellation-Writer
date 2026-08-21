# Run Receipt: CW-F1-SHELL-SPIKE-003

## Run contract

```yaml
run_id: CW-F1-SHELL-SPIKE-003
profile: computational_analysis
project_descriptor: choose the desktop shell for Constellation Writer
primary_outcomes:
  - falsifiable Tauri 2 and Electron controls sharing one renderer
  - Windows and macOS build/package/runtime evidence
  - ADR-0004 decision or explicit defer state
constraints:
  - no product UI scope
  - no hidden durable state
  - narrow native bridge
  - no fabricated accessibility or IME evidence
route: F1_architecture_coherent
```

## Inputs

- Roadmap Shared Execution Header + Sequence Item 3 work order.
- GitHub issue #3.
- ADR-0004 proposed Tauri candidate.
- Product Constitution, canonicality/state authority matrices, invariant and dependency registries.
- Current stacked F1 evidence branch.
- Current official Tauri 2 and Electron technical documentation, summarized in `spikes/desktop-shell/results/OFFICIAL_SOURCE_NOTES.md`.

## Actions

1. Compiled the ready-to-run prompt at `docs/delivery/RUN_PROMPT-03-DESKTOP_SHELL_SPIKE.md`.
2. Created stacked branch `spike/desktop-shell-decision` and PR #12.
3. Built one shared Vite/CodeMirror renderer with a deterministic 50,000-word fixture.
4. Built equivalent Electron and Tauri native controls around that renderer.
5. Added project-root traversal and symlink-escape negative controls.
6. Added Windows/macOS CI packaging and best-effort runtime instrumentation.
7. Preserved hosted-runner limitations instead of simulating them away.
8. Diagnosed and repaired missing Tauri bundle icon fixtures exposed by the first two CI attempts.
9. Achieved a green four-job desktop matrix at run `32085957984` and green foundation validation at `32085957973`.
10. Inspected all four measurement artifacts and recorded their digests.
11. Applied hard veto review before comparative judgement.
12. Updated ADR-0004 to select Electron for the F2 scaffold with explicit revisit triggers.

## Epistemic annotation

- Build/test/package outcomes: `epistemic_basis: measurement`, `validation_state: tested`.
- Hosted startup/render measurements: `epistemic_basis: measurement`, `validation_state: tested_on_hosted_runner_only`.
- Electron selection: `epistemic_basis: derived_result`, `work_function: decision`, `validation_state: candidate_pending_PR_promotion`.
- Physical IME/accessibility quality: `validation_state: unreviewed`, deliberately unresolved.
- Package-size and process-memory comparison: measured but marked non-equivalent where runtime/package ownership differs.

## Failures preserved

- Initial Tauri macOS attempt failed because the spike lacked the default bundle PNG expected by `generate_context!`.
- The next Windows Tauri attempt failed because `icon.ico` was missing. Platform bundle icons were added and the final matrix passed.
- These failures increased observed setup complexity but did not constitute a shell architecture veto.

## Omissions / limits

No claim is made that hosted CI validates:

- VoiceOver, Narrator or NVDA;
- real IME candidate-window behavior;
- real Windows high-contrast or macOS accessibility settings;
- human keyboard/menu ergonomics;
- Finder/Explorer drag/drop security edge cases;
- code signing, notarization, SmartScreen or Gatekeeper;
- six-hour writer comfort;
- representative-hardware startup or memory budgets.

## Decision

ADR-0004 selects Electron 43.2.0 as the F2 desktop scaffold. Tauri 2 remains the principal fallback and negative control. Shell-neutral domain boundaries are mandatory so the decision can be reversed without migrating project data.

## Validation

- Desktop shell workflow: `32085957984`, success, four matrix jobs.
- Foundation validator: `32085957973`, success.
- Evidence artifacts and digests are listed in `RESULTS_SUMMARY.yaml` and the spike report.

## Destination

- PR #12 review and merge closes issue #3.
- F1 remains open for #4, #5, issue #7 promotion, `CON-003`, adversarial closure and human approval.
- F2 inherits physical shell veto tests and real-hardware performance measurement.

## Review / invalidation triggers

Reopen this decision if Electron fails physical IME/accessibility, safe bridge, representative-hardware resource, distribution, or editor-engine controls. A shell change must not mutate canonical writer-owned formats.
