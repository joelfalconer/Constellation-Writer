# Run Receipt: CW-F1-COMPILE-SPIKE-005

## Run contract

```yaml
run_id: CW-F1-COMPILE-SPIKE-005
profile: computational_analysis
secondary_profile: system_design_strategy
project_descriptor: decide the Constellation-owned compile plan and Pandoc output-adapter boundary
primary_outcomes:
  - executable frozen compile plan plus minimal Workbench AST and source maps
  - deterministic direct Markdown and HTML plus isolated DOCX/EPUB adapter evidence
  - evidence-based ADR-0006 decision
constraints:
  - Manuscript Manifest remains assembly authority
  - Compile Profile cannot rewrite structure or semantic role
  - canonical Sheets are not parsed by Pandoc
  - adapter failure preserves Constellation-owned fallbacks
  - binary metadata drift is not confused with semantic nondeterminism
  - normal local execution does not depend on hosted CI
route: F1_architecture_coherent
```

## Research OS runtime

Research OS v0.4.1 was loaded from canonical `joelfalconer/research-os` for this consequential run.

Loaded runtime projection:

- Tier 0: `pipeline`, `profiles`, `methods`;
- Tier 1: `records`, `controls`, `context_lineage`, `criteria`.

The primary profile was `computational_analysis`: deterministic code owns YAML parsing, input hashing, manifest expansion, AST construction, rendering, source-map generation, adapter execution, artifact hashing, semantic comparison, and test evaluation. `system_design_strategy` governed the semantic-authority boundary, alternatives, reversal cost, and routing.

Hard gates were applied before candidate preference. The architecture was not allowed to select Pandoc merely because it supports many output formats.

## Corpus and source versions

Repository corpus:

- GitHub issue #5;
- ADR-0006 inherited as `proposed`;
- Compile Contract v0.1;
- Manuscript Manifest v0.2;
- Compile Profile JSON Schema;
- `tests/compile/golden-cases.yaml` CG-001 through CG-009;
- reference novel Manifest, Sheets, and draft HTML profile;
- canonical authority/invariant contracts loaded through the Shared Execution Header.

Current external sources:

- Pandoc official filters documentation describing reader → Pandoc AST → writer architecture;
- Pandoc official manual/reproducible-build documentation;
- official Pandoc 3.10.1 and 3.9.0.2 release assets and published SHA-256 values.

These external sources establish documented mechanics only. They do not establish Constellation-specific fitness.

## Context lineage and omissions

The Run Prompt 05 Shared Execution Header was inherited exactly from the already-preserved Run Prompt 04 header. Issue #5, ADR-0006, current compile/manuscript specifications, schema, golden cases, and reference fixture supplied the work-order details.

No unavailable historical research source was required for this architecture decision.

The artifact ZIP from the successful workflow was preserved by GitHub Actions as artifact `9441576333`. In-chat sandbox extraction was unavailable during this run, so evidence inspection used the decoded workflow job log plus artifact metadata/digest. This is recorded as a cognitive/tooling limitation rather than treated as missing evidence because the workflow emitted the tested receipts and comparisons into its logs and preserved the complete 41-file artifact.

## Method invocations

1. **Preflight:** bounded issue #5, declared hard authority gates, acceptance tests, non-goals and F1 route.
2. **Authority mapping:** assigned source, assembly, profile, compile-plan, AST, QA/source-map and adapter ownership explicitly.
3. **Executable model:** implemented frozen inputs, linear plan, minimal Workbench AST, direct Markdown/HTML, QA and source maps.
4. **Negative controls:** forbidden profile structural overrides, path escape, unsupported syntax, missing assets and adapter absence.
5. **Golden cases:** executed CG-001 through CG-009 intent.
6. **Repeatability control:** compiled the same frozen reference inputs twice and compared semantic/direct digests.
7. **Adapter control:** verified and executed Pandoc 3.10.1 and 3.9.0.2 against the same Constellation-owned representation.
8. **Semantic drift control:** compared binary hashes separately from normalized semantic round-trip hashes.
9. **Rival evaluation:** hard-vetoed Pandoc-as-canonical-authority; retained own-all-writers as a future viable alternative.
10. **Closure:** updated ADR-0006, Compile Contract v0.2, Manuscript Manifest authority, schema, evidence report, state and F1 route.

## Produced artifacts

- `docs/delivery/RUN_PROMPT-05-COMPILE_PIPELINE_SPIKE.md`
- `spikes/compile-pipeline/compile_spike.py`
- `spikes/compile-pipeline/test_compile_spike.py`
- `spikes/compile-pipeline/README.md`
- `spikes/compile-pipeline/OFFICIAL_SOURCE_NOTES.md`
- `.github/workflows/compile-pipeline-spike.yml`
- `spikes/compile-pipeline/results/COMPILE_SPIKE_REPORT-2026-08-21.md`
- `spikes/compile-pipeline/results/COMPILE_SPIKE_SUMMARY-2026-08-21.json`
- `docs/specifications/compile-contract-v0.2.md`
- reconciled `docs/specifications/manuscript-manifest-v0.2.md`
- updated `contracts/compile/compile-profile.schema.json`
- accepted ADR-0006 candidate and decision/state receipts

## Machine evidence

Evidence head: `68c4fc6564d8294c683211e3319025942da7666d`.

- Compile workflow `32468472581`: **success**.
- Foundation validation `32468472562`: **success**.
- Compile evidence artifact `9441576333`.
- Artifact digest: `sha256:75c5018dcb748f0e2a843445955068cf359f9c6f9872a0a047e69b22eee68b34`.
- Preserved files: 41.
- Golden/negative controls: 13/13 pass.

Repeated direct compile:

```yaml
plan_semantic_digest: 4e248c591d0060bed1b8ff81b2f687c9939f39851aae317f0121da6e364819ce
ast_semantic_digest: 482047b0677ca22c6ffba2df32a0d55d9d1cc610703636016dec91488db39b4b
markdown_sha256: 750942ba12534d7d62bbf423b818f0d4d793d07e4a4ffb15fe46d7f6b475d79c
html_sha256: 340f902bdcb7f48559073ab65e420d39e1d3780a7d8d5e31b4066505682e5813
source_map_sha256: c595054e2800180e083189792cb2bd4facb8a21f803fe64cc84af09712f7c410
direct_all_equal: true
```

Adapter controls:

```yaml
pandoc_current: 3.10.1
pandoc_prior: 3.9.0.2
docx:
  both_pass: true
  semantic_roundtrip_equal: true
  byte_equal: true
epub:
  both_pass: true
  semantic_roundtrip_equal: true
  byte_equal: false
semantic_roundtrip_sha256: 850f85e1f507a8a8e5d92ac73115a4a2df535a5dbeb1da3610680b29af949717
```

The EPUB byte difference is preserved as evidence that archive-byte identity and semantic equivalence are distinct validation dimensions.

## Epistemic annotation

- Test/CI outcomes: `epistemic_basis: measurement`, `work_function: experiment`, `validation_state: tested`.
- Frozen/direct digest equality: `epistemic_basis: derived_result`, `validation_state: machine_checked`.
- Pandoc version comparison: `epistemic_basis: measurement`, `validation_state: machine_checked`.
- Manifest/Profile authority rule: `epistemic_basis: derived_result`, `work_function: design`, `validation_state: candidate_pending_PR_promotion`.
- ADR-0006 selection: `epistemic_basis: derived_result`, `work_function: decision`, `validation_state: candidate_pending_PR_promotion`.
- Professional DOCX/EPUB quality/accessibility: `validation_state: unreviewed`.

## Candidate evaluation

### A. Constellation-owned plan/AST + pinned Pandoc output adapter

Selected. It survived all bounded authority, provenance, repeatability, adapter-version and adapter-failure hard gates.

### B. Pandoc as canonical compiler/AST owner

Rejected by hard architectural gate. It would collapse third-party conversion semantics into manuscript authority and weaken Constellation's source-map/QA ownership.

### C. Constellation-owned binary writers, no Pandoc

Retained as a serious fallback. It has a larger implementation/testing surface and no current evidence justifies taking that cost before a concrete adapter limitation appears.

## Decision

ADR-0006 accepts **Constellation-owned compile plan/Workbench AST plus Pandoc 3.10.1 as the pinned F2 DOCX/EPUB output-adapter baseline**.

This is not a generic endorsement of Pandoc as “the compiler.” Its value is deliberately quarantined to the replaceable edge of the architecture.

## Unresolved items

- production Markdown parser and full Workbench AST schema;
- bibliography/CSL ownership and implementation;
- richer Markdown extension policy;
- byte-addressed binary source maps;
- professional DOCX style/template fidelity;
- EPUB accessibility validation;
- PDF strategy;
- adapter distribution/licensing/signing/update policy;
- untrusted resource sandboxing;
- large-manuscript performance;
- professional writer/publisher output assay.

These are not F1 authority blockers unless later evidence shows the selected boundary cannot support them.

## Outcome observation contract

```yaml
outcome_observation_contract:
  target_phase: F2_and_F4
  observations:
    - compile_plan_source_map_survive_real_vertical_slice
    - professional_DOCX_output_meets_editorial_acceptance
    - EPUB_passes_selected_accessibility_validation
    - adapter_packaging_and_security_boundary_remain_viable
    - large_manuscript_compile_performance_within_budget
  trigger: executable_vertical_slice_or_professional_output_assay
  action_if_failed: reopen_ADR_0006_and_run_update_delta
```

No delayed outcome is claimed as already observed.

## Destination

- PR #14 promotion closes issue #5 if review accepts the decision.
- F1 then proceeds to `CON-003` mutation-ownership adjudication, adversarial architecture closure, clean promotion validation, and human gate decision.
- If F1 receives human approval, F2 vertical slice #6 inherits Electron, CodeMirror 6, the Constellation-owned compile plan/AST, direct Markdown/HTML, and the pinned Pandoc DOCX/EPUB adapter.

## Review / invalidation triggers

Reopen ADR-0006 if adapter output quality, accessibility, security, distribution, licensing, provenance, or version drift cannot satisfy product requirements without moving semantic authority into Pandoc. Replacing the adapter must not migrate writer-owned canonical state.
