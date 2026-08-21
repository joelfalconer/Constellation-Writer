# F1 Adversarial Architecture Closure — 2026-08-22

**Run:** `CW-F1-ARCH-CLOSURE-006`  
**Profile:** `adversarial_review` with `update_delta` and `system_design_strategy`  
**Depth:** standard, high-consequence governance  
**Execution mode:** `SEQUENTIAL_LENS_SIMULATION` because no isolated second model/context was available in this runtime  
**Destination:** human F1 Architecture Coherent gate decision

## Decision-relevant result

The architecture is **machine-review ready for the human F1 gate**. No critical architecture contradiction remains open after accepting ADR-0007, ADR-0009, and ADR-0010 and reconciling compile/mutation authority matrices.

This is not a claim that the F2 substrate is executable or production-ready. The repaired compile spike v0.2 still lacks a post-review local execution receipt, and multiple physical/product assays remain intentionally carried forward.

## Run contract

```yaml
project_descriptor: close Constellation Writer F1 architecture coherence after shell/editor/compile decisions
decision_context: determine whether architecture authority is coherent enough for explicit human F1 approval
primary_outcomes:
  - resolve CON-003 mutation ownership without competing canonical write paths
  - reconcile canonicality and authority after ADR-0006 compile decision
  - adversarially review accepted F1 scaffold and preserve serious rivals/revisit triggers
research_questions:
  - does every consequential durable state dimension have one declared owner
  - can PatchSession Recovery or CompileProfile silently become a competing authority
  - do accepted shell editor compile and identity choices preserve the product invariants
  - what must remain deferred to F2 or later rather than being falsely declared passed
research_corpus:
  - canonical constitution and sovereignty files
  - ADR-0004 through ADR-0010
  - contradiction and decision ledgers
  - Mutation Envelope PatchSession Recovery and compile specifications
  - PR 14 review findings and merged compile evidence
  - F1 readiness/current-state records
constraints:
  - no paid GitHub Actions dependency
  - do not claim unexecuted local validation passed
  - do not convert physical or professional assays into architecture evidence
  - preserve serious rivals and explicit falsifiers
non_goals:
  - production implementation
  - final Workbench AST design
  - professional DOCX EPUB acceptance
  - physical IME accessibility or six-hour writer validation
forbidden_inferences:
  - hosted evidence at an older commit validates later repaired code
  - architecture coherence proves runtime performance
  - proposed annotation storage has passed sync/reanchor tests
acceptance_tests:
  - zero open critical contradictions
  - no competing canonical assembly authority
  - one canonical mutation application authority
  - local user state remains noncanonical
  - identity format locked before durable prototype data
  - unresolved execution/product evidence remains visible
  - human gate remains explicit
```

## Research OS runtime

Canonical Research OS v0.4.1 was loaded from `joelfalconer/research-os`.

Tier 0 loaded: pipeline, profiles, methods. Tier 1 loaded: records, controls, context lineage, criteria, and telemetry. The adversarial review profile requires source-selection audit, rival-hypothesis testing, negative controls, and governed closure. The run also behaves as an update delta over prior F1 work rather than recomputing unaffected evidence. Full context, control, telemetry, omission, and method lineage is preserved in `docs/programme/RUN_RECEIPT-CW-F1-ARCH-CLOSURE-006.md`.

## Evidence and coverage summary

The current architecture corpus is internally coherent on the F1 decisions that materially constrain the F2 substrate:

| Dimension | Accepted authority / scaffold | Evidence state | F1 result |
|---|---|---|---|
| desktop shell | Electron | prior executable spike + ADR-0004 | accepted with physical revisit triggers |
| prose editor | CodeMirror 6 | prior executable spike + ADR-0005 | accepted with IME/accessibility/latency revisit triggers |
| manuscript assembly | Manuscript Manifest | contract + compile spike/ADR-0006 | accepted; CompileProfile cannot rewrite assembly |
| compile representation | Constellation-owned plan + Workbench AST | prior executable spike + ADR-0006 | accepted; production parser/AST deferred |
| DOCX/EPUB edge | pinned Pandoc adapter | versioned adapter evidence | accepted as replaceable edge only |
| canonical mutation application | Mutation Envelope | architecture contracts + adversarial authority review | accepted by ADR-0007; execution pending F2 |
| patch review/provenance | PatchSession | specification + ADR-0007 boundary | accepted jurisdiction |
| recovery preservation/restore mechanism | Recovery | specification + ADR-0007 boundary | accepted jurisdiction; restore applies through envelope |
| user interaction state | local user state | canonicality rationale + ADR-0009 | accepted noncanonical |
| durable object identity | typed UUIDv7 | invariant + ADR-0010 | accepted before persistent prototype data |
| annotations | dedicated annotation log direction | ADR-0008 | deferred to F2 validation; not yet canonical authority |

## Named maps

### Authority map

```text
Sheet body/identity -> Sheet files
Manuscript order/membership/role -> Manuscript Manifest
Export scope/render treatment -> Compile Profile
Frozen plan/AST/source map -> derived compile artifacts
Patch proposal/review -> PatchSession
Canonical application -> Mutation Envelope
Recovery material -> Recovery service
Mutation outcome history -> mutation event log
Cursor/scroll/panes/recent context -> local user state
Annotations -> authority deferred pending F2 executable assay
```

The prior stale authority entry `manuscript_manifest_with_compile_profile_override` has been removed. Manifest membership is now canonical; a profile may select an explicit export projection but cannot mutate assembly semantics.

The closure delta also caught a second authority-overreach during self-review: the Canonicality Matrix had temporarily named `annotation_log` as canonical despite ADR-0008 being deferred. That row was removed and annotations are now explicitly represented under deferred authority until F2 storage/reanchor/sync/compaction assays pass.

### Dependency map

```text
canonical files
    |
    v
mutation/recovery substrate
    |
    +------> derived catalog/indexes
    |
    +------> editor/binder/compile/continuity instruments
                 |
                 +------> optional AI/transmedia
```

No reviewed F1 decision requires derived state to become authoritative.

### Uncertainty map

The material uncertainties are execution and product-quality uncertainties, not unresolved ownership conflicts:

- post-review compile v0.2 local suite has not run in a repository checkout;
- physical editor/shell IME, bidi, assistive technology and real-hardware latency are not established;
- professional DOCX/EPUB fidelity and accessibility are not established;
- production Markdown parser, final Workbench AST, bibliography/CSL boundary and binary source-map granularity remain open;
- annotation log sync/file-count/reanchor/compaction behavior remains untested;
- professional writer assay has not run.

## Adversarial probes

### Probe A: PatchSession as universal transaction owner

**Rival:** PatchSession could own all application because AI and transformation already route through patches.

**Failure under test:** ordinary autosave, direct human edits, migration, import and restore would either be forced through an editorial review abstraction or create bypass paths. That produces architectural pressure toward multiple transaction models.

**Disposition:** rejected. PatchSession retains proposal/review/provenance jurisdiction only.

### Probe B: Recovery as transaction owner

**Rival:** make Recovery own writes because every consequential mutation needs rollback.

**Failure under test:** preservation/failure handling would become the primary mutation API, conflating ordinary writes with restoration and still leaving review-bearing PatchSessions beside it.

**Disposition:** rejected. Recovery prepares preservation/restore mechanisms; restore re-enters the Mutation Envelope.

### Probe C: separate transaction engines per subsystem

**Rival:** autosave, AI patch, migration and restore each use purpose-built transaction semantics.

**Hard veto:** violates one-owner authority, creates inconsistent stale-base/revision handling, and makes recovery guarantees operation-specific.

**Disposition:** rejected by non-compensatory architecture gate.

### Probe D: CompileProfile owns inclusion or semantic role

**Rival:** export profiles may be more convenient if they can override manuscript membership/role.

**Hard veto:** creates two manuscript authorities and makes the same work structurally different depending on an output profile.

**Disposition:** rejected. Profiles may project and render only.

### Probe E: cursor/scroll in canonical sidecars

**Rival:** portable state could improve multi-device continuity.

**Negative control:** delete local user state. Project truth must remain unchanged.

**Disposition:** rejected for canonical storage. Optional future handoff state may be portable but non-authoritative.

### Probe F: ULID or path/title identity

**Rivals:** ULID for readability; path/title-derived IDs for simple storage.

**Hard veto on path/title:** violates identity invariance under rename/move/reorder. ULID remains technically viable but offers no sufficient benefit over standard UUIDv7 to justify a second identity convention.

**Disposition:** typed UUIDv7 accepted.

### Probe G: promote annotation-log decision now

**Rival:** lock dedicated JSONL annotations at F1 because the architecture already prefers it.

**Counterexample:** file-count, sync conflicts, split/merge re-anchoring and compaction are precisely the behavior that has not been exercised.

**Disposition:** do not overclaim. Preserve ADR-0008 direction but defer acceptance to F2 evidence. The Canonicality Matrix must not name an annotation canonical owner until that decision is accepted.

## Hard-gate results

```yaml
critical_contradictions_open: 0
competing_manuscript_assembly_authority: false
competing_canonical_mutation_application_authority: false
derived_store_required_for_project_truth: false
AI_direct_canonical_write_authority: false
user_state_canonical_churn: false
identity_depends_on_title_path_or_placement: false
deferred_annotation_storage_presented_as_canonical: false
hosted_CI_required_for_project_validity: false
unexecuted_validation_claimed_passed: false
human_F1_decision_fabricated: false
```

## Accepted decisions at this closure

- ADR-0007: Mutation Envelope owns canonical transaction application.
- ADR-0009: cursor, scroll, panes, and recent context remain noncanonical local user state.
- ADR-0010: typed UUIDv7 is the durable object identity format.

ADR-0008 remains deferred to F2 validation. Existing ADR-0004, ADR-0005, and ADR-0006 remain accepted with their named revisit triggers.

## Validation posture without paid Actions

Hosted GitHub Actions is not a project validity gate. Workflows remain manual replication recipes. The canonical deterministic command is:

```bash
python tools/local_validate.py --suite all
```

This current runtime has repository read/write access but no checked-out repository execution environment. Therefore this closure does **not** claim a fresh local validation pass.

The post-review compile v0.2 code remains under the previously recorded narrow execution exception: architecture-decision promotion is allowed, but executable-substrate reliance is prohibited until a local suite passes. This limitation is carried directly into F2.

## Residual vetoes carried into F2/F4

These are deliberate unresolved controls, not hidden passes:

- a local deterministic all-suite receipt for the promoted substrate;
- physical editor/shell IME, bidi, accessibility and native-interaction assays;
- representative-hardware latency;
- mutation-envelope autosave latency and failure injection;
- archive/restore and conflict-loss tests;
- production parser / Workbench AST implementation;
- professional DOCX/EPUB fidelity and accessibility;
- Pandoc packaging, licensing, signing, security and update policy;
- annotation-log executable assay;
- professional writer assay.

## Epistemic annotation

- prior shell/editor/compile workflow results: `epistemic_basis: measurement`, `validation_state: tested` for the revisions actually executed;
- authority reconciliation and ADR-0007/0009/0010 selection: `epistemic_basis: derived_result`, `work_function: decision`, `validation_state: human_review_pending_gate`;
- compile v0.2 repair correctness: source-reviewed with targeted tests present, but `validation_state: unreviewed_by_execution` in the current revision;
- physical/professional quality claims: `validation_state: unreviewed` and explicitly carried forward.

## Machine closure decision

**Result: `ready_for_human_F1_gate`.**

The architecture has no remaining critical ownership contradiction. Serious rivals have either been rejected by explicit hard gates, retained as fallback/revisit options, or deferred with executable falsifiers.

The remaining gate is intentionally human because F1 commits the product to a high-reversal-cost substrate direction: Electron + CodeMirror 6 + Manifest-owned assembly + Constellation-owned compile plan/AST + replaceable Pandoc edge + typed UUIDv7 + Mutation Envelope mutation authority + noncanonical local user state.

## Human gate options

The owner may:

- **approve F1** and route to F2 vertical slice #6;
- **approve with explicit conditions** that become F2 entry gates;
- **reject/reopen** one or more ADRs and name the rival to re-evaluate.

No option is selected by this report.

## Route after approval

The first F2 action is to obtain a passing local `python tools/local_validate.py --suite all` receipt from a real repository checkout. Only then should the repaired compile spike be treated as executable substrate evidence.

F2 then builds the durable vertical slice around Electron, CodeMirror 6, Manifest-first project files, Mutation Envelope persistence/recovery, direct Markdown/HTML compile, and the pinned replaceable Pandoc edge.

## Review and invalidation triggers

Reopen F1 architecture coherence if implementation introduces a second canonical owner, requires SQLite/graph/UI state for project truth, forces compile semantics into Pandoc, makes autosave block the writing loop, or invalidates the accepted identity/assembly/mutation boundaries.
