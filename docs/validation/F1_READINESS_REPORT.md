# F1 Architecture Coherent Readiness v0.8

## Current readiness

```yaml
status: conditional_not_ready
F0: accepted_on_main
F1_reconciliation: PR_10_merged
benchmark_evidence_refresh: PR_11_merged_issue_7_closed
desktop_shell: ADR_0004_Electron_accepted_issue_3_closed
editor_engine: ADR_0005_CodeMirror_6_accepted_issue_4_closed
compile_architecture: ADR_0006_candidate_PR_14_review_repaired
compile_review_findings: 6_repaired_6_threads_resolved
validation_runtime: local_first_hosted_actions_optional_manual_only
post_repair_compile_suite: not_run_in_current_chat_runtime
critical_contradictions:
  - CON-003_mutation_ownership_candidate_resolution_pending_F1_confirmation
adversarial_F1_closure: pending_after_PR_14_promotion
vertical_slice_6: routed_to_F2_after_F1
human_F1_review: pending
```

## Accepted baseline

Canonical `main` includes the prior F1 stack and editor decision through merge `d24a6dff4a97d1a1ad3437c3f33abbae43978409`. Issues #3, #4, and #7 are closed. Electron and CodeMirror 6 are the accepted F2 shell/editor scaffolds, each with explicit physical revisit controls.

PR #14 is the current noncanonical compile-architecture candidate.

## F1 blocker register

| Blocker | Acceptance | Current state | Revisit trigger |
|---|---|---|---|
| #3 desktop shell | equivalent Tauri/Electron controls, hard veto review, ADR decision | **closed; Electron selected** | physical IME/accessibility, F2 real-hardware budget, editor-specific shell result |
| #4 prose editor | CodeMirror 6 + serious rival, longform/source/undo/selection/overlay evidence, ADR decision | **closed; CodeMirror 6 selected** | physical IME/accessibility/bidi, representative hardware, six-hour writer assay |
| #5 compile architecture | Workbench plan/AST proves deterministic semantic output, source mapping, QA, Pandoc isolation | **promotion-ready under recorded review-delta exception** | first F2 local execution receipt; output-quality/security/accessibility failure |
| #7 evidence lineage | historical gaps explicit; current benchmark claims use primary sources | **closed** | final SRC-DR-001 becomes available or consequential benchmark claim changes |
| `CON-003` mutation ownership | Mutation Envelope remains sole application/transaction owner | open critical | F1 closure and any F2 competing ownership evidence |
| adversarial F1 closure | serious rivals, authority contradictions, negative controls, residual vetoes reviewed | pending after PR #14 | any new critical contradiction |
| human F1 decision | owner accepts/rejects Architecture Coherent gate | pending | after adversarial closure receipt |

## Issue #5 compile result

The initial issue #5 executable established the intended authority boundary under machine execution:

- Constellation Writer owns frozen inputs, Manifest expansion, compile plan, Workbench AST, QA and source maps;
- the Manuscript Manifest owns order, membership, contextual placement role/title, and semantic break intent;
- Compile Profiles may select an explicit output projection and rendering treatment but may not rewrite assembly or semantic role;
- Pandoc remains a pinned, replaceable DOCX/EPUB output adapter rather than canonical compiler authority.

Evidence workflow `32468472581` passed 13/13 golden and negative controls at evidence head `68c4fc6564d8294c683211e3319025942da7666d`. Foundation validation `32468472562` also passed. Artifact `9441576333` preserves the original 41-file evidence bundle with digest `sha256:75c5018dcb748f0e2a843445955068cf359f9c6f9872a0a047e69b22eee68b34`.

Repeated direct compiles were equivalent. Verified Pandoc 3.10.1 and 3.9.0.2 adapters both produced semantically equal DOCX/EPUB round trips. EPUB bytes differed while semantic output remained equal, preserving the distinction between byte reproducibility and semantic determinism. An unavailable Pandoc binary preserved Constellation-owned fallbacks.

### Independent review delta

PR review then found six P1 implementation-fidelity defects:

1. inline comments could discard surrounding prose;
2. structural Manifest nodes could disappear;
3. duplicate placement IDs could create ambiguous source-map identity;
4. Compile Profile/Manifest manuscript identity was not bound;
5. referenced assets were not frozen before adapter execution;
6. role transforms were not actually applied during rendering.

The spike was revised to v0.2.0. All six defects were repaired, one named regression test was added for each finding, the repair locations were replied to in the PR, and all six review threads are resolved.

The post-review delta is recorded separately in `docs/programme/RUN_RECEIPT-CW-F1-COMPILE-SPIKE-005-REVIEW-DELTA.md` so the earlier tested evidence is not silently rewritten as evidence for later code.

## Validation runtime: no paid-CI dependency

GitHub Actions quota is outside the project's operating model. Hosted runner unavailability is therefore not a project failure and must not become a merge gate.

Automatic pull-request/push triggers are disabled for the foundation, compile, editor-engine, and desktop-shell workflows. The workflows remain available through `workflow_dispatch` as optional replication recipes.

The canonical deterministic route is now:

```bash
python -m pip install -r tools/validator/requirements.txt
python tools/local_validate.py --suite all
```

The runner emits `build/local-validation-receipt.json`. Policy and failure semantics are defined in `docs/validation/LOCAL_VALIDATION_POLICY.md`.

The current ChatGPT execution runtime has GitHub repository read/write access but no local repository checkout or outbound GitHub network path. The v0.2 post-review suite is therefore **not run** here. It is not described as passing. For F1 architecture promotion, this is a recorded validation exception because the architecture boundary already has executed evidence and the review delta is human-reviewed with targeted regression coverage. F2 must obtain a passing local receipt before relying on the repaired spike as executable substrate.

At the current PR head, GitHub reports no commit-status contexts and the PR remains mergeable. Absence of a hosted run is being treated as infrastructure unavailability, not as a green or red test result.

## Residual veto carry-forwards

These are not silently marked passed by F1 automation:

- shell physical IME and assistive-technology behavior;
- editor physical IME, bidi caret/selection, VoiceOver/Narrator/NVDA, high contrast and 200% zoom;
- representative-hardware editor latency replication;
- six-hour professional writer assay;
- professional DOCX/EPUB style and accessibility acceptance;
- adapter packaging/licensing/security/update policy;
- production-parser and large-manuscript compile performance.

They remain explicit F2/F4 revisit controls unless the adversarial F1 review finds one must be promoted to a blocking architecture gate.

## F1 entry and closure

F1 entry remains valid. F1 closure is not yet complete.

F1 may close only when:

- one canonical owner exists for every modeled v1 durable field;
- foundation schemas and fixtures remain coherent with the promoted architecture;
- PR #14 is promoted if the compile decision is accepted;
- `CON-003` is accepted, revised, or explicitly deferred with a falsifier and no competing application authority;
- architectural rivals remain preserved or explicitly retired with accepted evidence;
- no selected technology forces hidden canonical state, source-text loss, an accepted physical accessibility/IME veto, or compile-adapter authority leakage;
- adversarial F1 closure completes;
- human F1 approval is recorded in the gate receipt.

A paid hosted CI run is not an F1 closure condition.

## Route

1. Promote PR #14 under the explicit post-review validation exception if it remains mergeable and all blocking review threads remain resolved.
2. Close issue #5 as an architecture decision.
3. Adjudicate `CON-003` and run the F1 adversarial architecture closure.
4. Prepare the F1 gate receipt with pass/defer/fail findings and leave final human approval explicit.
5. If approved, route directly to F2 vertical slice #6.
6. Make the first F2 executable-substrate action a local `tools/local_validate.py --suite all` receipt before relying on the repaired compile spike.
7. Carry physical shell/editor and professional-output assays forward without pretending hosted CI already resolved them.
