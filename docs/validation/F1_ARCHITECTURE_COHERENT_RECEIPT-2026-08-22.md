# F1 Architecture Coherent Gate Receipt — 2026-08-22

**Gate:** F1 — Architecture Coherent  
**Machine closure state:** `complete`  
**Human decision:** `approved`  
**Decided by:** `joelfalconer`  
**Decided at:** `2026-08-22T01:50:00+10:00`  
**Run:** `CW-F1-ARCH-CLOSURE-006`

## Gate result

**F1 Architecture Coherent is accepted.**

The machine/adversarial closure established a coherent authority package with no open critical architecture contradiction. The human owner explicitly approved that package on 2026-08-22 and routed the project into F2 `Substrate Executable`.

The architecture names one canonical owner for manuscript assembly, one canonical application authority for mutation, one owner for Compendium canon state, and noncanonical boundaries for local user state and derived projections.

Approval is an architecture gate decision, not a claim that the executable substrate has already passed F2. Local deterministic validation remains the first F2 executable gate.

## Gate checklist

| Requirement | State | Evidence / note |
|---|---|---|
| F0 accepted baseline present | pass | canonical foundation already merged |
| desktop-shell architecture selected | pass | ADR-0004 Electron, with physical revisit triggers |
| editor-engine architecture selected | pass | ADR-0005 CodeMirror 6, with IME/accessibility/latency revisit triggers |
| compile authority selected | pass | ADR-0006, Manifest-owned assembly + Constellation plan/AST + replaceable Pandoc edge |
| critical mutation ownership resolved | pass | ADR-0007 accepts Mutation Envelope as sole canonical application authority |
| atomicity semantics coherent | pass | Product Constitution guarantees file-boundary atomic replacement where supported; multi-file operations are recovery-backed unless stronger transactional semantics are proven |
| durable identity direction locked before prototype data | pass | ADR-0010 typed UUIDv7 |
| volatile user state excluded from canonical project truth | pass | ADR-0009 |
| stale compile inclusion authority removed | pass | STATE_AUTHORITY_MATRIX gives Manifest sole assembly membership authority |
| Compendium canon-state owner unique | pass | `claim_record.canon_state`; no separate Canon State record in F1 model |
| competing PatchSession/Recovery transaction ownership removed | pass | PatchSession review, Mutation Envelope apply, Recovery preserve/restore mechanisms |
| deferred annotation storage not falsely canonical | pass | ADR-0008 deferred; Canonicality Matrix carries no premature annotation storage authority |
| open critical contradictions | pass | zero |
| serious rivals/revisit triggers preserved | pass | adversarial closure report + ADR falsifiers |
| hosted GitHub Actions required | pass | no; Actions is optional manual replication only |
| fresh local validation on closure revision | not_run | prior chat runtime lacked repository execution checkout |
| post-review compile v0.2 executable receipt | not_run | mandatory first F2 substrate gate |
| physical shell/editor assays | deferred | F2/F4 controls, not falsely marked passed |
| professional writer/output assays | deferred | later gate, not architecture evidence |
| human F1 decision | pass | explicitly approved 2026-08-22 |

## Accepted architecture package

```yaml
shell: Electron
editor_engine: CodeMirror_6
identity: typed_UUIDv7
source_of_truth:
  prose: readable_Sheet_files
  manuscript_assembly: Manuscript_Manifest
  metadata: canonical_sidecars_and_records
  derived_indexes: rebuildable_noncanonical
mutation:
  proposal_review: PatchSession_when_review_bearing
  canonical_application: Mutation_Envelope
  recovery_mechanisms: Recovery
  outcome_history: mutation_event_log
  atomicity:
    single_file: atomic_replacement_where_supported
    multi_file: recovery_backed_unless_stronger_transactional_guarantee_is_proven
compile:
  assembly_authority: Manuscript_Manifest
  export_projection_and_rendering: Compile_Profile
  semantic_intermediate: Constellation_owned_compile_plan_and_Workbench_AST
  direct_outputs: Markdown_and_HTML
  binary_edge: pinned_replaceable_Pandoc_adapter
user_state:
  cursor_scroll_panes_recent_context: local_noncanonical
compendium:
  posture: subordinate_minimal_boundary_until_later_product_gates
  claim_canon_state_owner: claim_record.canon_state
  annotations_storage_authority: deferred_pending_F2_assay
```

## PR closure-review delta

PR #15 review surfaced two additional P1 coherence defects before promotion:

1. Compendium `canon_state` still had two possible owners. The authority is now locked to `claim_record.canon_state`, the Claim schema imports the shared `CanonState` enum, the reference fixture is migrated, and the Claim Ledger explicitly rejects a separate F1 Canon State record.
2. ADR-0007's recovery-backed multi-file semantics conflicted with the Product Constitution's unqualified statement that canonical writes are atomic. The constitution now defines atomicity at the single-file replacement boundary where supported and explicitly requires recovery-backed, crash-detectable semantics for multi-file operations unless genuine cross-file transactions are proven.

These findings reinforce the closure method: zero-contradiction status is earned only after review, not inferred from the first coherent-looking model.

## Deferred decisions that do not block F1

ADR-0008 annotation storage remains deliberately deferred to F2 because file-count, sync, re-anchoring, split/merge, and compaction behavior are not yet measured. Other pending implementation decisions include final Workbench AST schema, citation/CSL ownership, snapshot placement, revision/hash coupling, search-engine upgrade path, and Pandoc packaging/security policy.

These are permitted to remain open because they do not create a competing canonical authority at F1 and each has a named later decision or falsifier.

## Validation boundary

The repository does not depend on paid hosted CI. The canonical deterministic validation command is:

```bash
python tools/local_validate.py --suite all
```

No prior unexecuted local validation is retroactively described as passing. F2 begins by obtaining a local deterministic receipt from a real repository checkout before relying on the repaired compile v0.2 code as executable substrate.

## Human decision record

```yaml
human_F1_decision:
  state: approve
  decided_by: joelfalconer
  decided_at: 2026-08-22T01:50:00+10:00
  conditions:
    - F2 begins with local deterministic validation
    - execute durable substrate vertical slice issue_6
  reopened_ADRs_or_topics: []
  rationale: approve F1 and route directly into F2 Substrate Executable
```

## Active route

F2 `Substrate Executable` begins with:

1. obtain a local `python tools/local_validate.py --suite all` receipt from a real checkout;
2. execute vertical slice issue #6 using the accepted architecture package;
3. exercise Mutation Envelope save/recovery/failure semantics;
4. run physical shell/editor IME/accessibility/native-interaction controls as the executable substrate becomes available.

## Review triggers

Reopen F1 if F2 requires a second canonical write authority, makes derived state necessary to interpret project truth, requires CompileProfile/Pandoc to redefine manuscript assembly, invalidates stable identity, requires a second Compendium canon-state owner, or proves that the Mutation Envelope cannot support non-blocking ordinary persistence and its documented file/multi-file recovery semantics.

## Outcome observation contract

```yaml
outcome_observation_contract:
  target_phase: F2
  expected_outcomes:
    - accepted_authority_boundaries_survive_real_vertical_slice
    - local_validation_receipt_passes_without_hosted_CI
    - mutation_envelope_supports_nonblocking_save_and_recovery
    - compendium_claim_canon_state_remains_single_owner
  owner: project_runtime_and_human_owner
  trigger: first_executable_vertical_slice
  return_path: reopen_F1_ADR_or_run_update_delta_if_falsified
```

No delayed outcome is claimed as already observed.
