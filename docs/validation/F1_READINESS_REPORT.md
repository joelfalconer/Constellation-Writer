# F1 Architecture Coherent Readiness v0.9

## Current readiness

```yaml
status: ready_for_human_decision
F0: accepted_on_main
F1_reconciliation: PR_10_merged
benchmark_evidence_refresh: PR_11_merged_issue_7_closed
desktop_shell: ADR_0004_Electron_accepted_issue_3_closed
editor_engine: ADR_0005_CodeMirror_6_accepted_issue_4_closed
compile_architecture: ADR_0006_accepted_PR_14_merged_issue_5_closed
compile_review_findings: 6_repaired_6_threads_resolved
validation_runtime: local_first_hosted_actions_optional_manual_only
post_repair_compile_suite: not_run_in_current_chat_runtime
critical_contradictions_open: 0
mutation_ownership: ADR_0007_accepted_Mutation_Envelope_sole_application_authority
user_state_canonicality: ADR_0009_accepted_noncanonical
identifier_format: ADR_0010_accepted_typed_UUIDv7
adversarial_F1_closure: complete_ready_for_human_gate
vertical_slice_6: routed_to_F2_after_human_F1_approval
human_F1_review: pending
```

## Decision-relevant result

F1 machine/adversarial closure is complete. The architecture is coherent enough to present to the owner for the explicit Architecture Coherent gate decision.

This is not a production-readiness claim. The repaired compile spike v0.2 still lacks a post-review local execution receipt, and physical/editorial/professional assays remain intentionally deferred.

## Accepted architecture baseline

Canonical `main` includes the shell, editor, and compile decisions through merge `cee98ddf7d3b32dd55aa3b4f5975d7d678df3bdb`.

| Architecture dimension | Accepted F1 direction | Validation posture |
|---|---|---|
| desktop shell | Electron | prior executable spike; physical revisit triggers preserved |
| prose editor | CodeMirror 6 | prior executable spike; IME/accessibility/latency revisit triggers preserved |
| identity | typed UUIDv7 | accepted before persistent prototype data |
| manuscript order/membership | Manuscript Manifest only | contract + compile authority evidence |
| compile semantic intermediate | Constellation-owned compile plan + Workbench AST | architecture accepted; production parser/AST deferred |
| binary compile edge | pinned replaceable Pandoc adapter | prior versioned executable evidence |
| canonical mutation application | Mutation Envelope | architecture accepted; executable save/recovery tests deferred to F2 |
| patch proposal/review | PatchSession when review-bearing | jurisdiction accepted |
| recovery | Recovery owns preservation/restore mechanisms | restore itself applies through Mutation Envelope |
| cursor/scroll/panes/recent context | local noncanonical user state | ADR-0009 accepted |
| annotations | dedicated log direction | deferred pending F2 storage/reanchor/sync assay |

## F1 blocker register

| Blocker | Current state | Revisit trigger |
|---|---|---|
| #3 desktop shell | **closed; Electron selected** | physical IME/accessibility, F2 real-hardware budget, editor-specific shell result |
| #4 prose editor | **closed; CodeMirror 6 selected** | physical IME/accessibility/bidi, representative hardware, six-hour writer assay |
| #5 compile architecture | **closed; PR #14 merged; ADR-0006 accepted** | first F2 local execution receipt; output-quality/security/accessibility failure |
| #7 evidence lineage | **closed** | final SRC-DR-001 becomes available or consequential benchmark claim changes |
| `CON-001` identifier format | **resolved for F1; typed UUIDv7** | implementation failure before public durable data |
| `CON-002` user-state canonicality | **resolved for F1; local noncanonical** | portable handoff requirement that cannot be served non-authoritatively |
| `CON-003` mutation ownership | **resolved for F1; Mutation Envelope sole application authority** | blocking autosave overhead or necessary second canonical write path in F2 |
| adversarial F1 closure | **complete** | any new critical contradiction |
| human F1 decision | **pending** | owner approval/rejection |

## Compile decision and review delta

Issue #5 established the intended compile boundary under machine execution:

- Constellation Writer owns frozen inputs, Manifest expansion, compile plan, Workbench AST, QA and source maps;
- the Manuscript Manifest owns order, membership, contextual placement role/title, and semantic break intent;
- Compile Profiles may select an explicit output projection and rendering treatment but may not rewrite assembly or semantic role;
- Pandoc remains a pinned, replaceable DOCX/EPUB output adapter rather than canonical compiler authority.

Evidence workflow `32468472581` passed 13/13 golden and negative controls at evidence head `68c4fc6564d8294c683211e3319025942da7666d`. Foundation validation `32468472562` also passed. Artifact `9441576333` preserves the original evidence bundle with digest `sha256:75c5018dcb748f0e2a843445955068cf359f9c6f9872a0a047e69b22eee68b34`.

Independent review then found six P1 implementation-fidelity defects. The spike was revised to v0.2.0, all six findings were repaired, six targeted regression tests were added, and all six review threads were resolved. The earlier executed evidence is not silently treated as execution evidence for the later repair delta.

PR #14 has now been merged and issue #5 closed. The merge is an architecture-decision promotion under the recorded narrow execution exception, not a claim that the repaired v0.2 implementation has passed a fresh local suite.

## Mutation ownership closure

The F1 adversarial review rejected three serious rival models:

- PatchSession as universal transaction owner;
- Recovery as transaction owner;
- separate subsystem-specific canonical transaction engines.

ADR-0007 accepts the Mutation Envelope as the sole canonical application/transaction authority.

The resulting jurisdiction is:

```text
proposal/review/provenance -> PatchSession when review-bearing
preflight/application/revision validation -> Mutation Envelope
preservation/snapshots/recovery bundles -> Recovery
restore application -> Mutation Envelope
outcome history -> mutation event log
derived rebuild -> downstream of successful mutation
```

The design remains falsifiable. F2 must prove that the shared envelope can support debounced/background direct save without blocking the writing loop and can handle interrupted multi-file mutation/recovery without creating a second write authority.

## Canonicality reconciliation

The stale authority statement allowing a Compile Profile override of manuscript inclusion has been removed.

Manifest membership is now canonical assembly truth. Compile Profiles may select an explicit export projection and target rendering treatment, but cannot redefine manuscript membership, order, or semantic role.

The mutation authority matrix now also separates PatchSession review history, Mutation Envelope application, mutation outcome history, and Recovery preservation instead of collapsing them into overlapping ownership.

## Adversarial closure

The closure review is preserved at:

- `docs/validation/F1_ADVERSARIAL_ARCHITECTURE_CLOSURE-2026-08-22.md`
- `docs/validation/F1_ARCHITECTURE_COHERENT_RECEIPT-2026-08-22.md`

The adversarial result is `ready_for_human_F1_gate`.

No critical contradiction remains open. Serious alternatives are either rejected by explicit hard gates, preserved as fallbacks/revisit options, or deferred with executable falsifiers.

## Validation runtime: no paid-CI dependency

GitHub Actions quota is outside the project's operating model. Hosted runner unavailability is not a project failure and must not become a merge gate.

Automatic pull-request/push triggers are disabled for the foundation, compile, editor-engine, and desktop-shell workflows. The workflows remain available through `workflow_dispatch` as optional replication recipes.

The canonical deterministic route is:

```bash
python -m pip install -r tools/validator/requirements.txt
python tools/local_validate.py --suite all
```

The runner emits `build/local-validation-receipt.json`. Policy and failure semantics are defined in `docs/validation/LOCAL_VALIDATION_POLICY.md`.

The current ChatGPT execution runtime has GitHub repository read/write access but no local repository checkout. The current closure revision and repaired compile v0.2 suite are therefore **not run** here. They are not described as passing.

The first F2 executable-substrate gate is a passing local receipt from a real repository checkout. F2 must not rely on the repaired compile implementation as executable substrate before that receipt exists.

## Deferred nonblocking decisions

These remain open without violating F1 architecture coherence because they do not create competing canonical authority and have explicit later tests:

- ADR-0008 annotation storage and compaction/reanchor/sync behavior;
- final Workbench AST schema;
- citation/bibliography/CSL ownership;
- revision-ID/hash coupling;
- snapshot storage location;
- SQLite FTS5 versus Tantivy upgrade path;
- Pandoc distribution/licensing/signing/security/update policy.

## Residual veto carry-forwards

These are not silently marked passed by F1:

- shell physical IME and assistive-technology behavior;
- editor physical IME, bidi caret/selection, VoiceOver/Narrator/NVDA, high contrast and 200% zoom;
- representative-hardware editor latency replication;
- Mutation Envelope autosave latency and failure-injection controls;
- archive/restore and external-conflict zero-loss tests;
- six-hour professional writer assay;
- professional DOCX/EPUB style and accessibility acceptance;
- adapter packaging/licensing/security/update policy;
- production parser and large-manuscript compile performance;
- annotation-log executable assay.

## F1 gate state

All machine/adversarial prerequisites for the human decision are now satisfied or explicitly deferred with falsifiers.

The final gate remains intentionally human because approval commits the project to a high-reversal-cost F2 direction.

The owner must choose one of:

```yaml
human_F1_decision:
  state: pending  # approve | approve_with_conditions | reject_reopen
  conditions: []
  reopened_ADRs_or_topics: []
  rationale: null
```

No decision is implied by this report.

## Route after approval

1. obtain a passing local `python tools/local_validate.py --suite all` receipt from a real repository checkout;
2. execute vertical slice issue #6 using Electron + CodeMirror 6 + Manifest-first files + Mutation Envelope persistence/recovery + Constellation-owned compile plan/AST;
3. run failure injection and restore/conflict controls;
4. run physical editor/shell IME/accessibility/native-interaction assays as the executable substrate becomes available;
5. keep professional writer/output assays and annotation storage validation as explicit later gates.
