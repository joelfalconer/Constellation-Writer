# F1 Architecture Coherent Gate Receipt — 2026-08-22

**Gate:** F1 — Architecture Coherent  
**Machine closure state:** `ready_for_human_decision`  
**Human decision:** `pending`  
**Run:** `CW-F1-ARCH-CLOSURE-006`

## Gate result

The machine/adversarial closure work is complete enough to present F1 to the owner for an explicit decision.

No critical architecture contradiction remains open. The architecture now names one canonical owner for manuscript assembly, one canonical application authority for mutation, and noncanonical boundaries for local user state and derived projections.

This receipt does **not** mark F1 passed. The owner must explicitly approve, approve with conditions, or reject/reopen the gate.

## Gate checklist

| Requirement | State | Evidence / note |
|---|---|---|
| F0 accepted baseline present | pass | canonical foundation already merged |
| desktop-shell architecture selected | pass | ADR-0004 Electron, with physical revisit triggers |
| editor-engine architecture selected | pass | ADR-0005 CodeMirror 6, with IME/accessibility/latency revisit triggers |
| compile authority selected | pass | ADR-0006, Manifest-owned assembly + Constellation plan/AST + replaceable Pandoc edge |
| critical mutation ownership resolved | pass | ADR-0007 accepts Mutation Envelope as sole canonical application authority |
| durable identity direction locked before prototype data | pass | ADR-0010 typed UUIDv7 |
| volatile user state excluded from canonical project truth | pass | ADR-0009 |
| stale compile inclusion authority removed | pass | STATE_AUTHORITY_MATRIX now gives Manifest sole assembly membership authority |
| competing PatchSession/Recovery transaction ownership removed | pass | PatchSession review, Mutation Envelope apply, Recovery preserve/restore mechanisms |
| open critical contradictions | pass | zero |
| serious rivals/revisit triggers preserved | pass | adversarial closure report + ADR falsifiers |
| hosted GitHub Actions required | pass | no; Actions is optional manual replication only |
| fresh local validation on closure revision | not_run | current ChatGPT runtime lacks repository execution checkout |
| post-review compile v0.2 executable receipt | not_run | mandatory first F2 substrate gate |
| physical shell/editor assays | deferred | F2/F4 controls, not falsely marked passed |
| professional writer/output assays | deferred | later gate, not architecture evidence |
| human F1 decision | pending | explicitly required below |

## Accepted architecture package presented to the human gate

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
```

## Deferred decisions that do not block F1

ADR-0008 annotation storage remains deliberately deferred to F2 because file-count, sync, re-anchoring, split/merge, and compaction behavior are not yet measured. Other pending implementation decisions include final Workbench AST schema, citation/CSL ownership, snapshot placement, revision/hash coupling, search-engine upgrade path, and Pandoc packaging/security policy.

These are permitted to remain open because they do not create a competing canonical authority at F1 and each has a named later decision or falsifier.

## Validation exception

The repository no longer depends on paid hosted CI. The canonical deterministic validation command is:

```bash
python tools/local_validate.py --suite all
```

The current runtime cannot execute that command against a checked-out repository. Therefore no fresh local pass is claimed for this closure revision.

The repaired compile spike v0.2 remains under the explicitly recorded non-production execution exception. Architecture decisions may proceed, but the repaired spike must not be relied on as executable F2 substrate until a passing local receipt exists.

## Human decision block

Choose exactly one:

```yaml
human_F1_decision:
  state: pending  # approve | approve_with_conditions | reject_reopen
  decided_by: null
  decided_at: null
  conditions: []
  reopened_ADRs_or_topics: []
  rationale: null
```

### If approved

Route to F2 `Substrate Executable`, beginning with:

1. obtain a passing local `python tools/local_validate.py --suite all` receipt from a real checkout;
2. execute vertical slice issue #6 using the accepted architecture package;
3. exercise Mutation Envelope save/recovery/failure semantics;
4. run physical shell/editor IME/accessibility/native-interaction controls as the executable substrate becomes available.

### If approved with conditions

Record conditions as F2 entry gates. Conditions must not be silently treated as already satisfied.

### If rejected/reopened

Name the ADR or authority boundary being reopened and preserve the accepted alternatives/fallbacks for a delta run.

## Review triggers

Reopen F1 if F2 requires a second canonical write authority, makes derived state necessary to interpret project truth, requires CompileProfile/Pandoc to redefine manuscript assembly, invalidates stable identity, or proves that the Mutation Envelope cannot support non-blocking ordinary persistence.

## Outcome observation contract

```yaml
outcome_observation_contract:
  target_phase: F2
  expected_outcomes:
    - accepted_authority_boundaries_survive_real_vertical_slice
    - local_validation_receipt_passes_without_hosted_CI
    - mutation_envelope_supports_nonblocking_save_and_recovery
  owner: project_runtime_and_human_owner
  trigger: first_executable_vertical_slice
  return_path: reopen_F1_ADR_or_run_update_delta_if_falsified
```

No delayed outcome is claimed as already observed.
