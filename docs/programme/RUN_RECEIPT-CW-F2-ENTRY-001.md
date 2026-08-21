# Run Receipt — CW-F2-ENTRY-001

**Date:** 2026-08-22  
**Phase:** F2 — Substrate Executable  
**Profile:** `system_design_strategy` + `computational_analysis` preflight  
**Depth:** standard  
**Destination:** durable substrate vertical slice issue #6

## Decision-relevant result

F1 `Architecture Coherent` was explicitly approved by the human owner at `2026-08-22T01:50:00+10:00`. The project is therefore authorized to enter F2 `Substrate Executable`.

The required local validation gate was attempted first. The current chat container could not obtain a repository checkout because outbound DNS could not resolve `github.com`. No validation command was run against a complete checkout and no pass/fail is claimed. This is recorded as **infrastructure unavailable**.

The local deterministic receipt remains mandatory before the repaired compile v0.2 implementation is relied on as executable substrate.

## Run Contract

```yaml
run_id: CW-F2-ENTRY-001
project_descriptor: Constellation Writer durable local-first professional writing workbench
decision_context: enter F2 after explicit human F1 approval and begin executable substrate proof
primary_outcomes:
  - record the human F1 approval canonically
  - attempt the mandatory local validation gate before substrate reliance
  - activate issue_6 durable substrate vertical slice
research_questions:
  - can the promoted architecture be exercised from real canonical files without hosted CI
  - can the first vertical slice prove persistence recovery manifest and catalog invariants
research_corpus:
  - F1 gate receipt and adversarial closure
  - CURRENT_STATE.yaml
  - ROADMAP.md
  - issue_6
  - tools/local_validate.py
constraints:
  - GitHub Actions must remain non_gating
  - no unexecuted validation may be described as passing
  - canonical project truth must remain file-owned and rebuildable
  - no SQLite-only durable field
  - zero silent loss
non_goals:
  - professional writer acceptance
  - final production Workbench AST
  - broad Compendium or AI implementation
forbidden_inferences:
  - infrastructure unavailability equals validation success
  - prior hosted evidence validates later unexecuted revisions
  - F1 approval equals F2 executable acceptance
risk_profile: high_reversal_cost_substrate
resource_profile: current_runtime_has_GitHub_connector_but_no_networked_local_checkout
output_contract:
  - accepted F1 receipt
  - F2 state transition
  - local validation preflight observation
  - issue_6 activation and implementation route
acceptance_tests:
  - human approval is recorded without changing its meaning
  - local validation state is explicit pass fail or infrastructure_unavailable
  - issue_6 hard gates remain intact
  - no hosted Actions dependency is introduced
```

## F1 human decision

```yaml
human_F1_decision:
  state: approve
  decided_by: joelfalconer
  decided_at: 2026-08-22T01:50:00+10:00
  conditions:
    - F2 begins with local deterministic validation
    - execute durable substrate vertical slice issue_6
```

## Local validation preflight

Canonical command:

```bash
python tools/local_validate.py --suite all
```

Attempted checkout command in the current execution container:

```bash
git clone --depth 1 https://github.com/joelfalconer/Constellation-Writer.git /tmp/Constellation-Writer
```

Observed result:

```text
fatal: unable to access 'https://github.com/joelfalconer/Constellation-Writer.git/': Could not resolve host: github.com
```

Classification:

```yaml
validation_attempt:
  state: infrastructure_unavailable
  stage: repository_checkout
  command_executed_against_repo: false
  local_validation_receipt_created: false
  hosted_CI_substitution_allowed: false
  executable_substrate_reliance_allowed: false
  recovery_path: rerun_from_any_real_checkout_with_local_dependencies_available
```

This does not block architecture work that does not claim executable validation, but it blocks declaring F2 substrate acceptance.

## Issue #6 execution contract

The vertical slice must prove this loop against real project files:

1. create/open the reference project;
2. read and validate Sheet frontmatter and sidecar;
3. edit a Sheet and replace the file atomically where supported;
4. persist and restore a recovery buffer;
5. render manuscript order from manifest IDs;
6. reorder a placement without changing Sheet prose;
7. build and delete a SQLite catalog;
8. rebuild the catalog from canonical files;
9. detect an external edit conflict and preserve both versions;
10. create a named snapshot and restore one Sheet.

Hard gates remain:

- zero silent loss;
- no SQLite-only durable field;
- rename/move preserves Sheet identity;
- recovery and conflict events produce receipts;
- validator passes before and after cache deletion;
- failure injection covers controlled write/termination boundaries.

## Epistemic annotation

- human F1 approval: `epistemic_basis: direct_observation`, `work_function: decision`, `validation_state: human_reviewed`;
- checkout failure: `epistemic_basis: direct_observation`, `work_function: measurement`, `validation_state: machine_checked`;
- F2 architecture route: `epistemic_basis: derived_result`, `work_function: action`, `validation_state: unreviewed_until_execution`.

## Route

```yaml
route:
  destination: build
  subject: issue_6_durable_substrate_vertical_slice
  owner: joelfalconer
  first_action: implement the smallest executable local-first persistence/recovery/catalog loop consistent with accepted contracts
  acceptance_test: issue_6 hard gates plus passing local validation receipt
  review_trigger: first executable vertical-slice PR and any authority contradiction
  rollback_or_deprecation_condition: reopen F1 if implementation requires competing canonical authority or derived state for project truth
```

## Outcome observation contract

```yaml
outcome_observation_contract:
  route_or_decision_id: F2_issue_6
  expected_outcome: accepted F1 authority boundaries survive executable persistence/recovery/catalog implementation
  metrics:
    - local_validation_pass
    - zero_silent_loss
    - cache_delete_rebuild_equivalence
    - recovery_receipt_completeness
    - conflict_preserves_both_versions
    - rename_move_identity_preservation
  owner_or_runtime: local_repository_runtime
  observation_schedule_or_trigger: first complete issue_6 execution
  return_path: update CURRENT_STATE and F2 receipt or reopen affected ADR
```

No delayed outcome is claimed as already observed.
