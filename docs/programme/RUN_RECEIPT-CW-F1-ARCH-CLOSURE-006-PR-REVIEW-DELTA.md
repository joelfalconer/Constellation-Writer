# Run Receipt Delta: CW-F1-ARCH-CLOSURE-006 PR Review

**Parent run:** `CW-F1-ARCH-CLOSURE-006`  
**Pull request:** #15  
**Profile:** adversarial review continuation  
**Validation state:** source-reviewed; fresh local execution not available in current harness

## Purpose

Preserve the material findings produced by PR #15 review after the initial F1 closure receipt, rather than silently rewriting the earlier machine-closure narrative.

## Review findings

### P1: Compendium canon-state ownership remained ambiguous

The State Authority Matrix still named `canon_state_record_or_claim_field_per_final_schema`, leaving two possible canonical owners despite the F1 rule that each durable field has exactly one owner.

**Disposition:** fixed by choosing `claim_record.canon_state` as the sole F1 authority.

Changes:

- State Authority Matrix now names `claim_record.canon_state`;
- Claim schema now requires `canon_state` and imports shared `CanonState`;
- reference Claim fixture migrated from `status` to `canon_state`;
- Compendium Claim Ledger explicitly states that no separate Canon State record exists in the F1 model;
- gate receipt records the unique ownership decision.

**Rationale:** canon state governs an atomic assertion, so storing it with the Claim minimizes authority surfaces and prevents a second lifecycle object from drifting away from the assertion it governs.

### P1: multi-file recovery semantics contradicted the atomicity law

ADR-0007 allowed interrupted multi-file operations to expose partial application recoverable through rollback/completion, while Product Constitution Article VII said without qualification that canonical writes are atomic.

**Disposition:** fixed by defining the actual guarantee rather than pretending ordinary filesystems provide universal cross-file transactions.

Changes:

- Product Constitution Article VII now guarantees atomic replacement at the **single-file boundary** where the supported filesystem provides the required primitive;
- multi-file mutations are explicitly operation-planned, recovery-backed, crash-detectable, and may not be reported as atomically committed without a real cross-file transaction guarantee;
- ADR-0007 contains matching atomicity semantics and F2 acceptance tests.

**Rationale:** product trust requires the application to state the guarantee it can actually uphold. Recovery-backed crash consistency is stronger than a fictional atomicity claim because partial state is detectable, explainable, and recoverable.

## Secondary self-review finding

Before these automated PR comments, sequential self-review also found that the Canonicality Matrix had prematurely promoted `annotation_log` to canonical ownership while ADR-0008 was deliberately deferred.

**Disposition:** the canonical row was removed. Annotations now live under `deferred_authority` until F2 file-count, sync, re-anchoring, split/merge, compaction, and portability assays pass.

## Validation impact

The repository validator source was inspected after the annotation deferral. Its authority-drift check iterates only `CANONICALITY_MATRIX.entries`; it does not require deferred fields to be canonical. It also validates the existing annotation fixture/schema independently, which is compatible with retaining that format as a candidate test surface rather than an accepted canonical owner.

The Claim schema migration is structurally compatible with the current validator: the reference Claim is schema-validated, the shared `CanonState` schema is already registered, and validator relationship checks do not depend on the removed Claim `status` field.

A fresh deterministic execution is still **not run** in this ChatGPT runtime. No pass is claimed.

## Review thread state

Both P1 findings were answered at their original review threads and resolved after the contract/schema repairs.

## Epistemic annotation

- PR findings: `epistemic_basis: direct_observation`, `work_function: analysis`, `validation_state: human_reviewed_in_PR_process`.
- Repair coherence: `epistemic_basis: derived_result`, `work_function: design`, `validation_state: source_reviewed_execution_pending`.
- Runtime correctness of the revised Claim schema and closure branch: `validation_state: not_run` in the current harness.

## Route

PR #15 may be promoted as the machine/adversarial F1 closure package once it remains mergeable and has no unresolved blocking review threads. Promotion does not constitute the owner's F1 approval.

The first executable-substrate gate after any human F1 approval remains:

```bash
python tools/local_validate.py --suite all
```

If that local gate fails, affected closure claims return through an update-delta run rather than being defended by the absence of hosted CI.
