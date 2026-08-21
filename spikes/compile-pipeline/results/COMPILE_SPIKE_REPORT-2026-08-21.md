# Compile Pipeline Spike Report — 2026-08-21

## Decision

**Accept ADR-0006 for the F2 scaffold:** Constellation Writer owns the frozen compile plan, Workbench AST, direct Markdown/HTML renderers, QA and source maps. Pandoc `3.10.1` is accepted as the pinned DOCX/EPUB output-adapter baseline behind that boundary. Pandoc does not own canonical state, manuscript structure, semantic roles, or source provenance.

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
route: F1_architecture_coherent
```

## Evidence environment

```yaml
repository: joelfalconer/Constellation-Writer
branch: spike/compile-pipeline-decision
evidence_head: 68c4fc6564d8294c683211e3319025942da7666d
workflow_run: 32468472581
foundation_validation_run: 32468472562
runner:
  os: Ubuntu 24.04.4 LTS
  image: ubuntu-24.04
  image_version: 20260816.277.1
python: 3.12.14
artifact:
  id: 9441576333
  digest: sha256:75c5018dcb748f0e2a843445955068cf359f9c6f9872a0a047e69b22eee68b34
  files_preserved: 41
```

Both the compile-spike workflow and existing foundation validator concluded `success` at the evidence head.

## Golden and negative controls

Thirteen tests passed in 0.099 seconds on the hosted runner:

| Control | Result |
|---|---|
| CG-001 Manifest order beats filesystem order | pass |
| CG-002 Excluded Sheet absent + reason preserved | pass |
| CG-003 Contextual title does not duplicate matching H1 | pass |
| CG-004 Scene break retained as semantic AST node | pass |
| CG-005 Comment excluded by default + QA explanation | pass |
| CG-006 Missing asset carries source locator | pass |
| CG-007 Source map covers authored output segments | pass |
| CG-008 Repeated frozen compile semantically equivalent | pass |
| CG-009 Unavailable Pandoc preserves direct fallbacks | pass |
| Compile Profile structure/role override hard gate | pass |
| Explicit profile scope does not mutate assembly inclusion | pass |
| Unsupported extension remains visible in QA | pass |
| Asset path escape blocks compile | pass |

The tests validate the architecture boundary, not full publishing fidelity.

## Repeated frozen compile

Two adapter-free compiles of the reference manuscript produced identical digests:

```yaml
plan_semantic_digest: 4e248c591d0060bed1b8ff81b2f687c9939f39851aae317f0121da6e364819ce
ast_semantic_digest: 482047b0677ca22c6ffba2df32a0d55d9d1cc610703636016dec91488db39b4b
markdown_sha256: 750942ba12534d7d62bbf423b818f0d4d793d07e4a4ffb15fe46d7f6b475d79c
html_sha256: 340f902bdcb7f48559073ab65e420d39e1d3780a7d8d5e31b4066505682e5813
source_map_sha256: c595054e2800180e083189792cb2bd4facb8a21f803fe64cc84af09712f7c410
direct_all_equal: true
```

This supports semantic determinism for the bounded plan/AST/direct-renderer path.

## Pinned adapter controls

The workflow downloaded official Linux amd64 Pandoc archives and verified published SHA-256 values before execution.

```yaml
pandoc_3_10_1:
  archive_sha256: 72948bf5784f560d5ad1876709daca27e0667f262da727bb33f77b58e52df2f5
  verification: pass
pandoc_3_9_0_2:
  archive_sha256: a69abfababda8a56969a254b09f9553a7be89ddec00d4e0fe9fd585d71a67508
  verification: pass
```

Both versions generated DOCX and EPUB successfully from the same Constellation-owned Markdown adapter representation.

| Target | 3.10.1 | 3.9.0.2 | semantic round-trip | byte equality |
|---|---|---|---|---|
| DOCX | pass | pass | equal | equal |
| EPUB | pass | pass | equal | different |

All four binary artifacts round-tripped to normalized plain text digest:

`850f85e1f507a8a8e5d92ac73115a4a2df535a5dbeb1da3610680b29af949717`

The current-version artifact hashes were:

```yaml
docx_3_10_1_sha256: 2a4287e9760d07e4fee9c57969bb33890283c76ab71be68d6267d7246f6dd011
epub_3_10_1_sha256: 7acb7a5d44eca87b8ca25ee4639f1f1515347eee55be41744cc473cceeb91855
```

The prior-version DOCX hash was identical to the current one. The prior-version EPUB hash was:

`57540ea7a5b15beefc08edc6f4a3f66a38923a7e79136ea2ffaeb5560ab45483`

The EPUB byte difference with equal semantic round-trip is an important result: byte identity alone would have created a false failure. Adapter invocations used a fixed `SOURCE_DATE_EPOCH` so documented timestamp nondeterminism did not dominate the comparison.

## Adapter-failure negative control

The compiler was invoked with a deliberately nonexistent Pandoc binary. Both DOCX and EPUB adapter records became `unavailable`, while the receipt remained `passed` and preserved nonempty:

- compile plan;
- Workbench AST;
- Markdown output;
- HTML output;
- source map;
- QA;
- compile receipt.

This directly falsifies the failure mode in which the external converter becomes the only viable compiler path.

## Authority result

The executable boundary preserves:

```yaml
authority:
  authored_source: Sheet
  assembly_order_membership_role: Manuscript_Manifest
  export_scope_target_treatment: Compile_Profile
  frozen_compile_plan: Constellation_Writer
  Workbench_AST: Constellation_Writer
  QA_source_maps: Constellation_Writer
  DOCX_EPUB_conversion: pinned_output_adapter
```

A test profile attempting `role_overrides` was blocked while the Manifest role remained unchanged. A separate scope test excluded an appendix from one output while preserving `assembly_include: true`. This is the key distinction between manuscript truth and output projection.

## Candidate evaluation

### Candidate A: Workbench plan/AST + Pandoc output adapter

**PASS / selected.** Survived all bounded hard gates and offers a replaceable path to professional binary outputs.

### Candidate B: Pandoc as canonical compiler or AST owner

**VETOED by architecture invariants.** It would collapse external conversion semantics into manuscript authority and weaken source-map/QA ownership. No convenience score can override this hard gate.

### Candidate C: Own DOCX/EPUB writers immediately

**Viable but deferred.** It preserves authority cleanly but carries a much larger implementation and validation surface. The current evidence does not justify paying that cost before a concrete adapter limitation appears.

The selected result is therefore a Pareto decision rather than a generic “Pandoc is best” claim: Constellation retains semantic sovereignty while borrowing a mature binary writer at the edge.

## Evidence limits and unresolved work

The run does not establish:

- a production Markdown parser;
- the final Workbench AST schema;
- bibliography/CSL completeness;
- tables/lists/math/raw-HTML policy beyond the bounded probe;
- byte-addressed reverse source maps inside DOCX/EPUB;
- professional reference DOCX styling;
- EPUB accessibility quality;
- PDF architecture;
- distribution/licensing/signing/update policy for the external binary;
- hardened untrusted-media/resource sandboxing;
- large-manuscript performance;
- professional writer/publisher acceptance.

These remain F2/F4 work or explicit revisit triggers. None is allowed to grant the adapter canonical authority.

## Validation state

```yaml
epistemic_basis:
  executable_boundary: measurement
  architecture_interpretation: derived_result
  external_pandoc_mechanics: source_assertion
work_function:
  executable_boundary: experiment
  ADR_0006: decision
validation_state:
  golden_controls: machine_checked
  reference_repeatability: machine_checked
  pandoc_version_comparison: machine_checked
  adapter_failure: machine_checked
  professional_output_quality: unreviewed
```

## Route

Promote ADR-0006 and Compile Contract v0.2 through PR review/merge, close issue #5, then run F1 contradiction/adversarial closure. If F1 receives human approval, route to F2 vertical slice #6 with:

- Electron scaffold;
- CodeMirror 6 editor scaffold;
- Manifest-first durable substrate;
- Constellation-owned compile plan/AST;
- direct Markdown/HTML;
- pinned Pandoc DOCX/EPUB adapter;
- preserved physical IME/accessibility and professional-workflow veto tests.
