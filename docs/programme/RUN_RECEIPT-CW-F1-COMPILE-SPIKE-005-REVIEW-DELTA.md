# Review Delta: CW-F1-COMPILE-SPIKE-005

**Parent receipt:** `RUN_RECEIPT-CW-F1-COMPILE-SPIKE-005.md`  
**Date:** 2026-08-21  
**Purpose:** preserve the post-machine-evidence code-review delta without rewriting the earlier tested evidence

## Trigger

Independent PR review of #14 found six P1 defects in the first executable compile spike. The findings did not falsify the selected ADR-0006 authority boundary, but they did show that the first implementation did not yet faithfully exercise several parts of that boundary.

The findings were:

1. inline HTML comments could discard authored prose on the same line;
2. included structural Manifest nodes could vanish from the compile plan/AST;
3. duplicate placement IDs could create ambiguous source-map identities;
4. Compile Profile `manuscript_id` was not bound to the selected Manifest;
5. referenced assets were not frozen before Pandoc adapter execution;
6. declared `role_transforms` were not applied during direct rendering.

## Repair delta

`spikes/compile-pipeline/compile_spike.py` was revised to v0.2.0.

The repair:

- masks comment spans while preserving surrounding prose and source-line topology;
- retains supported structural node kinds and emits explicit semantic AST blocks;
- rejects duplicate placement IDs as a blocking identity error;
- rejects Manifest/Profile manuscript identity mismatch;
- hashes and stages exact referenced asset bytes before adapter invocation;
- rejects external asset URIs until an explicit policy exists;
- gives Pandoc only staged compile-output resources rather than live canonical project assets;
- applies supported Compile Profile role treatments during Markdown and HTML rendering;
- preserves the Manifest as sole assembly and semantic-role authority.

Six named regression tests were added to `spikes/compile-pipeline/test_compile_spike.py`, one for each review finding.

All six review threads were replied to with the repair and regression location and then resolved.

## Validation-runtime change

The project no longer treats paid GitHub Actions capacity as a gate dependency.

Automatic pull-request/push triggers were removed from the foundation, compile, editor, and desktop-shell workflows. The workflows remain available through `workflow_dispatch` as optional replication recipes if hosted capacity is available later.

The repository now owns a local deterministic entrypoint:

```bash
python tools/local_validate.py --suite all
```

Policy is recorded in `docs/validation/LOCAL_VALIDATION_POLICY.md`.

### Current validation state

The pre-review architecture evidence remains valid within its tested scope:

- compile workflow `32468472581`: passed at evidence head `68c4fc6564d8294c683211e3319025942da7666d`;
- foundation workflow `32468472562`: passed at the same evidence epoch;
- Pandoc 3.10.1 / 3.9.0.2 adapter comparison and failure-fallback evidence remain preserved in artifact `9441576333`.

Those runs **do not validate the later v0.2 repair commit** and are not represented as doing so.

GitHub Actions is unavailable as a current execution route because hosted quota is outside the project's operating model. This is classified as `hosted_ci_unavailable`, not `failed`.

The ChatGPT execution environment used for this review has GitHub repository read/write access but no local repository checkout or outbound GitHub network path. Therefore the newly added local deterministic suite is `not_run` in this review context. No passing result is fabricated.

## Promotion exception and rationale

PR #14 is an F1 architecture-decision spike, not production compiler promotion. The architecture decision itself has prior executed evidence, and the six post-review defects were implementation-fidelity defects that have been repaired under source review with targeted regression tests.

For this F1 promotion only, the absence of a post-repair execution receipt is accepted as a **recorded validation exception** rather than a reason to depend on paid hosted CI. The repaired spike remains `human_reviewed / not_run_post_repair` until the first available local checkout executes `tools/local_validate.py`.

This exception does not convert unexecuted tests into passed tests and does not authorize production reliance on the spike.

## Required carry-forward

Before F2 treats the repaired compile spike as executable substrate, run:

```bash
python -m pip install -r tools/validator/requirements.txt
python tools/local_validate.py --suite all
```

and preserve the resulting `build/local-validation-receipt.json` or an equivalent immutable receipt.

If that local run fails any repaired regression, reopen ADR-0006 implementation acceptance and fix the spike before using it as substrate. The architectural authority decision may be revisited separately if the failure reveals a boundary problem rather than an implementation bug.

## Epistemic annotation

```yaml
post_review_repairs:
  epistemic_basis: direct_observation
  work_function: design
  validation_state: human_reviewed
regression_tests:
  epistemic_basis: direct_observation
  work_function: experiment
  validation_state: unreviewed_not_run
hosted_actions_current_state:
  epistemic_basis: source_assertion
  work_function: description
  validation_state: unavailable_not_failure
adr_0006_architecture_decision:
  epistemic_basis: derived_result
  work_function: decision
  validation_state: tested_pre_review_plus_human_reviewed_delta
```

## Route

PR #14 may be promoted under this explicit exception if it remains mergeable and no blocking review thread remains. Issue #5 may then close as an architecture decision.

The first F2 executable-substrate gate must consume a passing local validation receipt before relying on the repaired spike implementation.
