# Run Receipt — CW-F2-VERTICAL-SLICE-006-CANDIDATE

**Original run:** 2026-08-22  
**Adversarial hardening delta:** 2026-08-29  
**Issue:** #6 — durable Sheet persistence, manifest assembly, and recovery  
**Phase:** F2 — Substrate Executable  
**Profile:** `system_design_strategy` + `computational_analysis` + `adversarial_review`  
**State:** `candidate_not_full_repo_validated`

## Decision-relevant result

The first durable-substrate candidate remains **unaccepted as F2**. It now includes the review-driven hardening required to exercise stale-base races, post-commit outcome ambiguity, abrupt process death, concurrent rollback divergence, canonical-path symlink rejection, corrupt SQLite rebuild, snapshot corruption, permission/ENOSPC failure and no-clobber moves.

The mandatory full-repository proof contract is still:

```bash
python tools/local_validate.py --suite all
```

That command has **not** run against this PR from a complete checkout in the current ChatGPT runtime. Direct checkout remains unavailable from the execution container. GitHub Actions is not substituted and remains optional/manual-only. F2 therefore remains open.

## Implemented substrate

### Vault

`packages/vault/core.py` now treats canonical path safety as part of the data contract:

- traversal and project-root escape are rejected;
- symlinked path components are rejected;
- canonical Sheet, sidecar, manifest and inventory files must be regular non-symlink files;
- Sheet identity is resolved from durable IDs rather than filename/path.

### Mutation application

The stable `packages.mutation.core` API is now backed by separated atomic/application/reconciliation modules.

For guarded writes with an expected base hash, supported platforms use an atomic exchange/replace-with-backup primitive so the exact file displaced at commit time is retained. The displaced version is checked against the expected base. A commit-time mismatch is rolled back while retaining the proposed application bytes separately rather than silently overwriting the external edit.

Platform candidates are:

- Linux: `renameat2(..., RENAME_EXCHANGE)`;
- macOS: `renamex_np(..., RENAME_SWAP)`;
- Windows: `ReplaceFileW` with backup.

The displaced backup must remain on the same filesystem as the canonical target on POSIX. Unsupported semantics fail closed.

Post-commit errors are represented as `applied_unconfirmed` when the intended bytes are already canonical. They are not mislabeled as failed operations.

### Recovery-backed multi-file work

Before canonical application, operation bundles persist before images, intended after images, hashes and target state. During application, target progress and displaced versions are persisted. Startup reconciliation can classify an interrupted target as `before`, `after` or `divergent`.

Rollback restores a target only when the current canonical hash still equals the operation's applied hash. If another editor changed it, those divergent bytes are preserved and the operation enters recovery-required state rather than overwriting them.

Hard process termination is part of the candidate fault model, not merely an in-process exception.

### Recovery and snapshots

Snapshot restore now verifies:

- snapshot project identity;
- exact path membership in `snapshot.yml`;
- object identity when present;
- source file is canonical and non-symlinked;
- source bytes match the checksum recorded in the snapshot manifest before any canonical mutation;
- restored target bytes match that recorded checksum.

A corrupt snapshot therefore blocks restore before mutation.

### Manifest and derived catalog

Manifest order remains canonical assembly authority. Reorder is applied through the Mutation Envelope and is assayed against unchanged Sheet prose hashes.

SQLite remains under `.workbench/cache/catalog.sqlite`, is derived entirely from canonical files, and is assayed for deletion and corrupt-file rebuild equivalence.

### Canonical move

The candidate move operation uses a no-clobber link/unlink strategy rather than `exists()` followed by an overwriting rename. Destination collision fails closed. Cross-filesystem or unsupported no-clobber moves also fail closed at this gate rather than risking replacement.

## Candidate deterministic evidence

A Linux isolated candidate-source harness was executed after the adversarial repairs:

```text
python -m unittest discover -s tests/substrate -p 'test_*.py' -v
Ran 24 tests
OK
```

The 24-test observation combines the existing substrate cases and the new review-hardening regression suite. It includes:

- typed UUIDv7;
- Sheet/sidecar recovery and guarded save;
- precommit stale-base race with external-version preservation;
- post-commit `applied_unconfirmed` semantics;
- permission and ENOSPC failure before commit;
- hard single-file process exit + restart reconciliation;
- Manifest reorder without prose mutation;
- SQLite delete/rebuild and corrupt-cache rebuild;
- three-version conflict preservation;
- snapshot restore and corrupt-snapshot rejection;
- symlinked Sheet rejection;
- move identity preservation and destination no-clobber;
- synchronous multi-file rollback;
- hard multi-file process exit + persisted-bundle recovery;
- rollback under a concurrent divergent edit without overwriting that edit.

This is `measurement/tested` evidence for the isolated Linux candidate source only. It is **not** the complete-repository acceptance receipt and does not establish the Windows/macOS implementations.

## Vertical-slice receipt semantics

`tools/f2_vertical_slice.py` now emits `cw_f2_vertical_slice_receipt_v2` and distinguishes:

- `vertical_slice_state`; from
- `f2_gate_state`.

Even a passing vertical-slice command leaves F2 at `awaiting_full_local_validation_and_explicit_gate_decision` until the full local proof contract has run.

The vertical slice now binds its success predicate to the substrate fault matrix and also exercises corrupt-catalog rebuild, controlled permission/ENOSPC failures, post-commit outcome semantics and a stale-base race.

## Hard-gate posture

| Issue #6 hard gate | Candidate state | F2 acceptance |
|---|---|---|
| zero silent loss | conflict, stale-race and divergence-preservation controls implemented | pending full local receipt + platform replication |
| no SQLite-only durable field | delete/rebuild + corrupt-rebuild controls implemented | pending full local receipt |
| rename/move preserves Sheet identity | tested in isolated candidate | pending full local receipt |
| recovery/conflict receipts | implemented | pending full local receipt |
| validator before/after cache deletion | wired into vertical slice | **not yet executed on complete PR checkout** |
| controlled failure injection | abrupt exits + race + permission + ENOSPC + postcommit controls implemented | pending full local receipt + platform replication |

## Residual falsifiers

The following remain deliberately open:

1. Execute `python tools/local_validate.py --suite all` from a complete checkout with validator dependencies installed.
2. Physically exercise guarded replacement on supported Windows and macOS filesystems; the current new exchange implementation is tested only on Linux.
3. Exercise filesystem/mount edge cases including same-device backup assumptions and cross-volume moves.
4. Re-run adversarial PR review against the hardened head and repair any new blocking findings.
5. Only after those controls, adjudicate the explicit F2 gate. A mergeable PR is not itself F2 acceptance.

## Epistemic annotation

```yaml
isolated_linux_substrate_tests:
  epistemic_basis: measurement
  work_function: experiment
  validation_state: tested
  count: 24
  result: pass
branch_implementation:
  epistemic_basis: derived_result
  work_function: design
  validation_state: machine_checked_only_in_isolated_candidate_source
full_repository_validation:
  validation_state: unreviewed
  command: python tools/local_validate.py --suite all
  state: not_run
F2_gate:
  validation_state: unreviewed
  state: open
```

## Route

```yaml
route:
  destination: F2_validation
  next_actions:
    - rerun adversarial review on the hardened PR head
    - repair blocking findings
    - obtain complete local checkout execution
    - run python tools/local_validate.py --suite all
    - preserve build/local-validation-receipt.json and F2_VERTICAL_SLICE_RECEIPT.json
    - explicitly adjudicate F2 Substrate Executable
  rollback_or_reopen:
    - reopen affected F1 ADR if executable evidence falsifies an accepted authority boundary
```
