# Run Receipt — CW-F2-VERTICAL-SLICE-006-PR-REVIEW-DELTA

**Date:** 2026-08-29  
**PR:** #18  
**Issue:** #6  
**Profile:** `adversarial_review` + `computational_analysis`  
**Execution mode:** sequential review plus deterministic isolated fault harness

## Purpose

Capture the blocking findings from the first Codex review of PR #18, the repairs made in response, the evidence actually obtained, and the control that remains unresolved.

The first review evaluated commit `aaed430620` and produced nine material findings. Eight are implementation defects suitable for repair in this PR. The ninth is the full local-validation gate and remains intentionally unresolved until a complete checkout can execute the proof contract.

## Review delta

| Finding | Severity | Repair | Candidate evidence |
|---|---|---|---|
| stale-base check raced with replacement | P1 | guarded commit now uses atomic exchange/ReplaceFile with displaced-version verification; mismatch rolls back and preserves proposed bytes | stale-race regression passes on Linux candidate |
| post-replace failure falsely reported `failed` | P1 | post-commit outcome becomes `applied_unconfirmed` when intended bytes are canonical | postcommit regression passes |
| multi-file crash lacked intended hashes/progress | P1 | bundles persist before/after bytes, hashes, per-target state and displaced versions | hard-exit restart reconciliation passes |
| rollback could overwrite concurrent edit | P1 | rollback compares current hash to applied hash; divergent bytes are preserved and recovery is required | concurrent-divergence regression passes |
| canonical scans accepted symlinks | P1 | canonical path resolver rejects symlink components/files in Sheet, sidecar, manifest and inventory scans | symlinked-Sheet regression passes |
| vertical-slice receipt omitted key fault gates | P1 | slice is bound to substrate fault matrix and explicitly exercises corrupt SQLite, permission/ENOSPC, postcommit and stale-race cases; gate state is separate from slice state | candidate fault matrix passes |
| snapshot restore trusted current snapshot bytes | P2 | restore verifies project/path/object/hash from `snapshot.yml` before mutation | corruption regression passes |
| move could clobber raced destination | P2 | no-clobber link/unlink move; collision fails closed | destination-collision regression passes |
| full local proof contract not run | P1/gate | **not waived**; `python tools/local_validate.py --suite all` remains required | `not_run` in current runtime |

## Additional architecture correction

The guarded replacement implementation was separated into atomic, operation-journal and reconciliation modules while preserving `packages.mutation.core` as the stable import surface. This keeps OS-specific commit machinery from swallowing Mutation Envelope and recovery semantics into one file.

For POSIX guarded writes, the displaced recovery backup is required to be on the same filesystem as the canonical target. Unsupported exchange semantics fail closed. Cross-platform behavior remains an explicit physical F2 assay rather than an inferred property.

## Candidate evidence

After the hardening delta, an isolated Linux candidate source executed:

```text
python -m unittest discover -s tests/substrate -p 'test_*.py' -v
Ran 24 tests
OK
```

This evidence is machine/test evidence for the isolated candidate source. It does not establish that the complete repository head passes foundation, compile and substrate suites together, and it does not establish macOS/Windows filesystem behavior.

## Validation exception

```yaml
full_local_validation:
  command: python tools/local_validate.py --suite all
  state: not_run
  reason: current_chat_runtime_has_no_complete_repository_checkout_execution_path
  classification: infrastructure_unavailable
  substitute_github_actions: prohibited
  F2_acceptance_allowed: false
```

GitHub Actions quota availability is not treated as a project validity signal.

## Thread disposition rule

Review findings 1–8 may be resolved only after the repaired files are present on the PR head and the corresponding regression is recorded. Finding 9 remains open until the full local receipt exists. A re-review of the hardened head is required before F2 acceptance.

## Route

1. reply to and resolve repaired review threads 1–8;
2. leave the full-validation thread open;
3. request a fresh adversarial review of the hardened head;
4. repair any new blocking findings;
5. execute full local validation from a complete checkout;
6. preserve receipts;
7. make an explicit F2 decision.
