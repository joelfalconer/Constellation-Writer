# Run Prompt 05: Workbench Compile Plan and Pandoc Adapter Spike

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
- Treat this as a Research OS `system_design_strategy` plus `computational_analysis` run.
- Establish a compact run contract in the run receipt.
- Prefer primary/official technical documentation when current external facts matter.
- Create a dedicated branch.
- Build the smallest executable artifact that can falsify the candidate decision.
- Add fixtures and negative controls before claiming success.
- Run deterministic tests locally or in any available runner; CI is evidence transport, not the only executable path.
- Update ADRs/contracts only to the extent supported by evidence.
- Open a focused PR with measured results, unresolved risks, rollback path, and gate destination.
- Do not merge your own PR unless explicitly instructed.

## Work Order: Compile plan and output-adapter decision spike (#5)

TASK: Execute issue #5 and decide ADR-0006 by proving or falsifying the boundary between Constellation Writer's compiler and Pandoc as a pinned output adapter.

The spike must preserve one-owner-per-semantic-dimension authority:
- the Sheet owns authored source and intrinsic identity;
- the Manuscript Manifest owns assembly order, placement, inclusion, semantic role, contextual title behavior, and semantic break intent;
- the Compile Profile may select an explicit export scope and map resolved semantics to target-format treatment, but may not silently rewrite manuscript order, membership, or semantic role;
- the Workbench compile plan freezes resolved inputs before rendering;
- the Workbench AST and QA/source-map layer remain Constellation-owned;
- Pandoc receives only a controlled adapter representation and owns no canonical state or manuscript semantics.

Build and test at minimum:
- reference-manuscript expansion into a linear compile plan;
- frozen input hashes for manifest, profile, and every included Sheet;
- a minimal Workbench AST with stable semantic segment IDs;
- direct Markdown and HTML renderers independent of Pandoc;
- source maps from output segments to placement, Sheet, frozen revision digest, and source span;
- comments excluded by default with explainable QA;
- semantic scene breaks and title/first-heading de-duplication;
- front/back matter and chapter/scene role handling in synthetic golden controls;
- footnotes, citation markers, assets, missing assets, and unsupported syntax;
- repeated frozen compile equivalence;
- a deliberately unavailable Pandoc adapter preserving compile plan, QA, source map, Markdown, and HTML fallback;
- DOCX and EPUB through a pinned Pandoc release;
- one prior Pandoc release comparison, using semantic round-trip checks rather than byte identity as the only criterion;
- `SOURCE_DATE_EPOCH` when invoking Pandoc so nondeterministic timestamps do not masquerade as semantic drift.

Decision method:
- Apply hard vetoes first: source loss, non-explainable inclusion/order changes, semantic-role leakage into the adapter, broken source-map provenance, adapter failure destroying Constellation-owned outputs, or target output requiring Pandoc to parse canonical Sheets directly.
- Compare surviving architectures on semantic ownership, determinism, source-map continuity, QA explainability, adapter isolation, output quality, version drift, implementation cost, and reversal cost.
- Do not accept Pandoc because it supports many formats, and do not reject it merely because conversions can be lossy. Measure the controlled boundary.
- Treat binary byte identity as useful but subordinate to semantic equivalence for archive formats containing metadata.

Deliverables:
- executable compile-plan/Workbench-AST spike;
- direct Markdown and HTML renderers;
- pinned Pandoc DOCX/EPUB adapter control;
- repeatability and adapter-version comparison scripts/results;
- golden-case and negative-control tests;
- QA and source-map artifacts;
- Compile Contract authority correction if the evidence supports it;
- ADR-0006 updated to accepted/rejected/deferred with evidence;
- compile-service scaffold recommendation;
- PR linked to #5.

## Run Contract

```yaml
run_id: CW-F1-COMPILE-SPIKE-005
profile: computational_analysis
secondary_profile: system_design_strategy
project_descriptor: decide the Constellation-owned compile plan and Pandoc output-adapter boundary
primary_outcomes:
  - executable frozen compile plan plus minimal Workbench AST and source maps
  - deterministic direct Markdown and HTML plus isolated DOCX/EPUB adapter evidence
  - evidence-based ADR-0006 decision or explicit defer state
research_corpus:
  - issue_5
  - ADR_0006
  - compile_contract_and_manuscript_manifest_specs
  - compile_profile_and_identity_contracts
  - reference_novel_and_compile_golden_cases
  - current_official_Pandoc_documentation_and_release_information
constraints:
  - manuscript_manifest_remains_assembly_authority
  - compile_profile_does_not_rewrite_structure_or_semantic_role
  - canonical_Sheets_are_not_parsed_by_Pandoc
  - adapter_failure_must_preserve_constellation_owned_fallbacks
  - generated_binary_metadata_must_not_be_confused_with_semantic_nondeterminism
  - CI_or_hosted_runners_are_not_required_for_normal_local_execution
acceptance_tests:
  - golden_cases_CG_001_through_CG_009_are_executed_or_exactly_explained_if_out_of_scope
  - repeated_frozen_inputs_produce_equivalent_compile_plan_AST_markdown_and_html
  - source_map_covers_every_authored_output_segment_with_placement_sheet_revision_and_span
  - missing_asset_and_unsupported_syntax_are_explainable_QA_findings
  - Pandoc_failure_preserves_compile_plan_markdown_html_QA_and_source_map
  - pinned_and_prior_Pandoc_versions_are_compared_for_semantic_DOCX_and_EPUB_output
route: F1_architecture_coherent
```
