# F1 Architecture Coherent Readiness v0.7

## Current readiness

```yaml
status: conditional_not_ready
F0: accepted_on_main
F1_reconciliation: PR_10_merged
benchmark_evidence_refresh: PR_11_merged_issue_7_closed
desktop_shell: ADR_0004_Electron_accepted_issue_3_closed
editor_engine: ADR_0005_CodeMirror_6_accepted_PR_13_merged_issue_4_closed
compile_architecture: ADR_0006_accepted_candidate_PR_14_open
critical_contradictions:
  - CON-003_mutation_ownership_candidate_resolution_pending_F1_confirmation
adversarial_F1_closure: pending_after_PR_14_promotion
vertical_slice_6: routed_to_F2_after_F1
human_F1_review: pending
```

## Accepted baseline

Canonical `main` now includes the prior F1 stack and editor decision through merge `d24a6dff4a97d1a1ad3437c3f33abbae43978409`. Issues #3, #4, and #7 are closed. Electron and CodeMirror 6 are therefore the accepted F2 shell/editor scaffolds, each with explicit physical revisit controls.

The current noncanonical candidate is PR #14 for issue #5, the compile architecture decision.

## F1 blocker register

| Blocker | Acceptance | Current state | Revisit trigger |
|---|---|---|---|
| #3 desktop shell | equivalent Tauri/Electron controls, hard veto review, ADR decision | **closed; Electron selected** | physical IME/accessibility, F2 real-hardware budget, editor-specific shell result |
| #4 prose editor | CodeMirror 6 + serious rival, longform/source/undo/selection/overlay evidence, ADR decision | **closed; CodeMirror 6 selected** | physical IME/accessibility/bidi, representative hardware, six-hour writer assay |
| #5 compile architecture | Workbench plan/AST proves deterministic semantic output, source mapping, QA, Pandoc isolation | **closure-ready on PR #14 review/merge; ADR-0006 selected boundary** | adapter quality/accessibility/security/distribution/version drift or source-map requirement that breaks isolation |
| #7 evidence lineage | historical gaps explicit; current benchmark claims use primary sources | **closed** | final SRC-DR-001 becomes available or consequential benchmark claim changes |
| `CON-003` mutation ownership | Mutation Envelope remains sole application/transaction owner | open critical | F1 closure and any F2 competing ownership evidence |
| adversarial F1 closure | serious rivals, authority contradictions, negative controls, residual vetoes reviewed | pending after PR #14 | any new critical contradiction |
| human F1 decision | owner accepts/rejects Architecture Coherent gate | pending | after machine/adversarial closure receipt |

## Issue #5 compile result

Sequence item 5 built an executable frozen compile plan and minimal Workbench AST around the existing reference manuscript. The decision workflow `32468472581` passed, and the existing foundation validator remained green in `32468472562` at evidence head `68c4fc6564d8294c683211e3319025942da7666d`.

Artifact `9441576333`, digest `sha256:75c5018dcb748f0e2a843445955068cf359f9c6f9872a0a047e69b22eee68b34`, preserves 41 evidence files.

### Golden and authority controls

Thirteen tests passed, covering CG-001 through CG-009 plus explicit authority/security controls:

- Manifest order beat filesystem order;
- excluded material stayed absent and explainable;
- duplicate contextual title/first H1 was suppressed;
- scene break survived as semantic intent;
- comments remained profile-governed and source-located in QA;
- missing assets produced source-located QA;
- every authored test output segment mapped to placement, Sheet, frozen revision digest and source span;
- repeated frozen compile was semantically equivalent;
- unavailable Pandoc preserved the Constellation-owned plan/AST/Markdown/HTML/source-map path;
- profile structure/role override was rejected as a hard gate;
- profile scope removed one placement from output without changing `assembly_include`;
- unsupported syntax stayed visible in QA;
- asset path escape blocked the compile.

### Deterministic direct path

Two frozen reference compiles produced identical plan, AST, Markdown, HTML and source-map digests. `direct_all_equal` was `true`.

This supports the F1 authority model in which the compiler remains useful without an external binary adapter.

### Pandoc version control

The workflow downloaded and verified official release archives for Pandoc `3.10.1` and `3.9.0.2` before execution. Both generated DOCX and EPUB successfully from the same Constellation-owned adapter representation.

- DOCX: semantic round-trip equal, bytes equal.
- EPUB: semantic round-trip equal, **bytes differed**.
- All four binary outputs round-tripped to normalized semantic digest `850f85e1f507a8a8e5d92ac73115a4a2df535a5dbeb1da3610680b29af949717`.

The EPUB result preserves the distinction between semantic determinism and archive-byte identity. Adapter invocations fixed `SOURCE_DATE_EPOCH` so documented timestamp nondeterminism did not masquerade as semantic drift.

### Decision

ADR-0006 therefore selects:

> **Constellation owns frozen inputs, Manifest expansion, the compile plan, Workbench AST, QA, source maps and direct Markdown/HTML. Pandoc 3.10.1 is a pinned DOCX/EPUB output adapter only.**

Compile Contract v0.2 and Manuscript Manifest v0.2 now make the Manifest the sole assembly authority. Compile Profiles can select an explicit export projection and rendering treatment but cannot reorder, change membership, or redefine semantic roles.

This decision does not promote the bounded spike parser into the production compiler. Final Workbench AST schema, production Markdown parser, citation/CSL boundary, binary reverse-map granularity, professional DOCX/EPUB fidelity/accessibility, and adapter distribution/security policy remain explicit F2/F4 work.

Evidence:

- `spikes/compile-pipeline/results/COMPILE_SPIKE_REPORT-2026-08-21.md`
- `spikes/compile-pipeline/results/COMPILE_SPIKE_SUMMARY-2026-08-21.json`
- `docs/programme/RUN_RECEIPT-CW-F1-COMPILE-SPIKE-005.md`

## F1 entry and closure

F1 entry remains valid. F1 closure is **not yet ready**, but the technology/evidence spike sequence is now materially complete subject to PR #14 promotion.

F1 may close only when:

- one canonical owner exists for every modeled v1 durable field;
- foundation schemas and fixtures remain machine checked at the promotion head;
- PR #14 is reviewed/merged if the compile decision is accepted;
- `CON-003` is accepted, revised, or explicitly deferred with a falsifier and no competing application authority;
- architectural rivals remain preserved or explicitly retired with accepted evidence;
- no selected technology forces hidden canonical state, source-text loss, an accepted physical accessibility/IME veto, or compile-adapter leakage;
- adversarial F1 closure passes;
- human F1 approval is recorded in the gate receipt.

## Residual veto carry-forwards

These are not silently marked passed by F1 hosted automation:

- shell physical IME and assistive-technology behavior;
- editor physical IME, bidi caret/selection, VoiceOver/Narrator/NVDA, high contrast and 200% zoom;
- representative-hardware editor latency replication;
- six-hour professional writer assay;
- professional DOCX/EPUB style and accessibility acceptance;
- adapter packaging/licensing/security/update policy;
- production-parser and large-manuscript compile performance.

They remain explicit F2/F4 revisit controls unless the adversarial F1 review finds one must be promoted to a blocking architecture gate.

## Route

1. Review and merge PR #14 if the issue #5 evidence and ADR-0006 boundary are accepted.
2. Independently adjudicate `CON-003` mutation ownership against current schemas, state machines, Mutation Envelope, PatchSession and Recovery contracts.
3. Run the F1 adversarial architecture closure review across ADR-0004/0005/0006, authority matrices, invariants, schema validation, known gaps and carried vetoes.
4. Re-run clean promotion validation at the closure head.
5. Prepare `F1_ARCHITECTURE_COHERENT_RECEIPT.md` with explicit pass/defer/fail findings and leave the final human gate decision to the owner.
6. If human F1 approval is recorded, route immediately to F2 vertical slice #6 with Electron + CodeMirror 6 + Manifest-first durable substrate + Constellation-owned compile plan/AST + direct Markdown/HTML + pinned Pandoc DOCX/EPUB adapter.
