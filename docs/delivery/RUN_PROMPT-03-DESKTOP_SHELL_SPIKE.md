# Run Prompt 03: Desktop Shell Decision Spike

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

## Work Order: Desktop shell decision spike (#3)

TASK: Execute issue #3 and decide ADR-0004 through measured Tauri 2 vs Electron evidence.

Build equivalent minimal shell controls. Do not build the product UI yet.

Both controls must include:
- editor placeholder using the same web editor component;
- native open/save dialogs;
- project-directory permission boundary;
- filesystem watcher;
- native menu and keyboard shortcut;
- clipboard and drag/drop;
- crash/restart fixture;
- safe bridge call for an atomic-file-write placeholder.

Test at minimum on Windows and macOS where the available environment permits, recording any environment limitation explicitly:
- startup time and idle memory;
- packaged size;
- 50k-word document rendering baseline;
- IME composition and mixed-script/bidi;
- accessibility tree, keyboard navigation, 200% zoom, high contrast;
- native dialog and menu behavior;
- symlink/path escape and permission boundary;
- crash/restart event handling;
- dev/build complexity and signing/package implications.

Decision method:
- Apply hard vetoes first: accessibility failure, unsafe file boundary, unacceptable editor behavior, or materially unfixable platform inconsistency.
- Compare surviving options on writer experience, reliability, security boundary, implementation complexity, packaging, and reversal cost.
- Do not reward Tauri merely for smaller binaries or Electron merely for ecosystem familiarity.

Deliverables:
- two bounded spike implementations;
- repeatable benchmark scripts/results;
- platform limitation log;
- ADR-0004 updated to accepted/rejected/deferred with evidence;
- desktop scaffold recommendation;
- PR linked to #3.

## Run Contract

```yaml
run_id: CW-F1-SHELL-SPIKE-003
profile: computational_analysis
project_descriptor: choose the desktop shell for the local-first professional writing workbench
primary_outcomes:
  - falsifiable Tauri 2 and Electron controls sharing one renderer
  - cross-platform build/runtime measurements where CI permits
  - evidence-based ADR-0004 decision or explicit defer state
research_corpus:
  - issue_3
  - ADR_0004
  - product_constitution_and_authority_contracts
  - current_official_Tauri_and_Electron_documentation
constraints:
  - no_product_UI_scope
  - no_hidden_durable_state
  - narrow_native_bridge
  - preserve_unmeasured_accessibility_and_IME_as_open_risks
acceptance_tests:
  - both_shells_build_on_windows_and_macos_or_record_exact_environment_failure
  - path_escape_negative_controls_pass
  - same_50k_word_renderer_is_used_by_both_shells
  - CI_artifacts_preserve_metrics_and_failures
  - ADR_decision_does_not_claim_unmeasured_behavior
route: F1_architecture_coherent
```
