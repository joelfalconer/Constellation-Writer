# Run Receipt — CW-F2-VERTICAL-SLICE-006-CANDIDATE

**Date:** 2026-08-22  
**Issue:** #6 — durable Sheet persistence, manifest assembly, and recovery  
**Phase:** F2 — Substrate Executable  
**Profile:** `system_design_strategy` + `computational_analysis`  
**State:** `candidate_not_full_repo_validated`

## Decision-relevant result

The first executable substrate candidate is now implemented across the Vault, Mutation, Recovery, Manuscript, and Catalog boundaries, with a deterministic vertical-slice harness and a new `substrate` suite in `tools/local_validate.py`.

The candidate is **not yet accepted as F2 executable substrate**. The current ChatGPT runtime still cannot obtain a complete repository checkout because outbound DNS cannot resolve `github.com`. Therefore the mandatory full-repository command has not run on this branch and no full local pass is claimed.

A prototype-equivalent isolated harness was executed in the local sandbox before promotion of the candidate source. Nine substrate tests passed, covering typed UUIDv7 generation, Sheet/sidecar loading, recovery-buffer save, single-file failure before replacement, manifest reorder without prose mutation, SQLite delete/rebuild equivalence, three-version conflict preservation, snapshot restore, rename/move identity preservation, and recovery-backed multi-file rollback.

After finding that direct execution of `tools/f2_vertical_slice.py` initially lacked the repository root on `sys.path`, the harness was repaired. A local import smoke test (`python tools/f2_vertical_slice.py --help`) then passed and the nine isolated tests were rerun successfully. This is useful candidate evidence, but it remains distinct from the required full-repository receipt.

## Implemented substrate

### Vault

`packages/vault/core.py` provides:

- safe project-relative path resolution with traversal/symlink-escape rejection;
- native YAML loading without timestamp coercion;
- Sheet frontmatter parsing and content hashing;
- recursive Sheet discovery by stable ID rather than filename/path;
- duplicate Sheet and sidecar detection;
- Sheet/sidecar identity and kind reconciliation;
- project and manuscript discovery helpers.

### Mutation Envelope application

`packages/mutation/core.py` provides:

- typed UUIDv7 operation IDs;
- stale-base SHA-256 validation;
- same-directory temporary write, file `fsync`, `os.replace`, and directory `fsync` where supported;
- mutation receipts for applied and failed operations;
- recovery-backed multi-file operation plans that persist before-images before writes;
- controlled failure injection and reverse-order rollback of already-applied targets;
- governed canonical move with stable object identity.

No cross-file atomicity is claimed.

### Recovery

`packages/recovery/core.py` provides:

- checksummed editor recovery buffers;
- named point-in-time snapshots with file hashes;
- restore through the Mutation Envelope with a pre-restore snapshot;
- preservation of base, application, and external versions for conflicts;
- conflict and restore receipts.

### Manuscript

`packages/manuscript/core.py` provides:

- manifest loading;
- recursive placement projection;
- ordered Sheet-ID resolution;
- governed root-placement reorder through the Mutation Envelope.

Sheet prose is not the assembly authority and is not rewritten by reorder.

### Derived catalog

`packages/catalog/core.py` provides a rebuildable SQLite projection under `.workbench/cache/catalog.sqlite` containing:

- project metadata needed to identify the rebuild source;
- Sheet ID/path/title/kind/status and hashes;
- manuscript identity/path/hash;
- placement/manuscript relationships and order.

The catalog is built from canonical files, may be deleted, and has a deterministic logical projection digest for rebuild comparison.

### Executable issue #6 harness

`tools/f2_vertical_slice.py` copies the reference project into a disposable build directory and exercises:

1. validator before mutation;
2. Sheet/frontmatter/sidecar read;
3. recovery-buffer round trip and governed save;
4. Manifest order and reorder without prose mutation;
5. SQLite build/delete/validator/rebuild equivalence;
6. external three-version conflict preservation;
7. named snapshot and one-Sheet restore;
8. rename/move identity preservation;
9. single-file controlled write failure;
10. recovery-backed multi-file controlled failure and rollback;
11. validator after the vertical slice;
12. machine-readable F2 vertical-slice receipt.

## Deterministic validator integration

`tools/local_validate.py` now accepts:

```bash
python tools/local_validate.py --suite substrate
```

and includes the substrate tests and reference vertical slice in:

```bash
python tools/local_validate.py --suite all
```

The runner remains local-only, does not install dependencies, does not require network access, and does not treat GitHub Actions availability as evidence.

## Candidate test observation

```yaml
candidate_local_observation:
  runtime: isolated_sandbox_prototype_equivalent_source
  tests:
    command: python -m unittest discover -s tests/substrate -p 'test_*.py' -v
    count: 9
    passed: 9
    failed: 0
  import_smoke:
    command: python tools/f2_vertical_slice.py --help
    state: passed_after_repo_import_root_fix
  full_repository_validation:
    command: python tools/local_validate.py --suite all
    state: not_run
    reason: current_runtime_cannot_checkout_repository_due_outbound_DNS
```

## Hard-gate status

| Issue #6 hard gate | Candidate evidence | F2 acceptance state |
|---|---|---|
| zero silent loss | conflict test preserves base/app/external; recovery buffers/snapshots present | candidate, full vertical slice pending |
| no SQLite-only durable field | catalog delete/rebuild logical equivalence test | candidate, full validator pending |
| rename/move preserves Sheet identity | stable-ID move test | candidate |
| recovery/conflict receipts | receipt-producing tests and harness | candidate |
| validator before/after cache deletion | wired into executable harness | **not yet executed on complete repo** |
| controlled failure injection | single-file pre-replace and multi-file rollback tests | candidate |

## Known limitations / review targets

- `os.replace` behavior and directory durability still require platform-specific execution on supported filesystems.
- The `after_replace` failpoint represents post-replacement failure and needs recovery semantics before it can be treated as zero-loss crash proof.
- Multi-file recovery is currently synchronous rollback after an injected exception; real process termination between targets must be exercised from persisted bundle state.
- Snapshot file copying is an F2 implementation boundary, not yet a finalized archive/storage design.
- Conflict detection here consumes explicit base/app/external bytes; filesystem watcher/editor integration is later work.
- SQLite schema is deliberately minimal and derived; FTS/search is not required for this slice.
- Physical Electron/CodeMirror behavior is outside this substrate candidate.

## Epistemic annotation

- isolated nine-test result: `epistemic_basis: measurement`, `work_function: experiment`, `validation_state: tested` for the isolated prototype-equivalent harness;
- candidate branch implementation: `epistemic_basis: derived_result`, `work_function: design`, `validation_state: unreviewed_by_full_repo_execution`;
- full F2 acceptance: `validation_state: unreviewed` until a real checkout produces the required receipt.

## Route

```yaml
route:
  destination: build
  subject: issue_6_candidate
  next_actions:
    - open implementation PR and run adversarial code/authority review
    - repair blocking review findings
    - run python tools/local_validate.py --suite all from a complete local checkout
    - preserve build/local-validation-receipt.json and F2_VERTICAL_SLICE_RECEIPT.json
    - only then adjudicate F2 Substrate Executable acceptance
  acceptance_test:
    - full local validation passes
    - issue_6 hard gates pass
    - no competing canonical authority is introduced
  rollback_or_reopen:
    - reopen affected F1 ADR if implementation falsifies an accepted authority boundary
```
