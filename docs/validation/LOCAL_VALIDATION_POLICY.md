# Local Validation Policy

**Status:** active operational policy  
**Applies when:** hosted CI is unavailable, quota-limited, disabled, or intentionally not used

## Purpose

Constellation Writer must remain buildable, reviewable, and promotable without paid GitHub Actions capacity. Hosted CI is useful evidence transport and cross-platform replication, but it is not the authority that determines whether repository work is valid.

The canonical gate input is a reproducible validation receipt tied to the code under review, not the presence of a green hosted badge.

## Core rule

> Infrastructure unavailability is not a test failure.

A GitHub Actions run that is absent, skipped, queued indefinitely, or unable to start because of account quota is recorded as `hosted_ci_unavailable`. It must not be converted into `failed`, and it must not block work when an equivalent deterministic validation path is available locally.

An actual executed test failure remains a failure regardless of where it ran.

## Canonical local command

From the repository root:

```bash
python -m pip install -r tools/validator/requirements.txt
python tools/local_validate.py --suite all
```

The validation runner does not install dependencies and does not require network access once dependencies are present. It emits:

```text
build/local-validation-receipt.json
```

The receipt records the runtime, commands, return codes, output digests, output tails, and aggregate acceptance state.

### Compile-only validation

```bash
python tools/local_validate.py --suite compile
```

### Optional local Pandoc adapter check

```bash
python tools/local_validate.py --suite compile --pandoc /path/to/pandoc
```

No Pandoc download is attempted by the local runner. Adapter evidence is optional unless a work order specifically requires a current binary-format replication.

## Validation classes

### 1. Deterministic repository validation

May run locally and may satisfy promotion gates when the relevant suite passes:

- schema and reference validation;
- contract tests;
- parsing and hashing checks;
- compile golden and negative controls;
- repeatability and source-map checks;
- deterministic fixture transforms.

### 2. Hosted cross-platform replication

GitHub Actions or another hosted executor may provide additional Windows/macOS/Linux evidence. This is additive evidence, not a universal prerequisite.

If hosted capacity is unavailable, preserve the last valid hosted evidence and carry forward only the claims it actually supports. Do not pretend a newer commit was hosted-tested.

### 3. Physical and human assays

IME behavior, assistive technology, native clipboard/drag, real-hardware latency, long-session writer comfort, and professional acceptance require their own target runtime or human protocol. Neither local unit tests nor GitHub Actions may be used to claim these passed without the actual assay.

## Promotion rule

A change may be promoted without GitHub Actions when all of the following are true:

1. the relevant deterministic local suite has a passing receipt tied to the reviewed revision, or the change is documentation-only and explicitly exempted;
2. code review has no unresolved blocking finding;
3. any hosted-only or physical evidence not rerun is named as carried-forward or unavailable rather than silently assumed;
4. required canonicality, provenance, mutation, and rollback controls remain satisfied;
5. the pull request is mergeable under repository protection rules.

If the current execution environment cannot run the local suite, that limitation must be recorded. Review may continue, but an unexecuted local suite must not be described as passing.

### Explicit execution exception

A non-production, reversible architecture-decision or falsification spike may be promoted without a post-change execution receipt only when **all** of these additional conditions are recorded:

- the reason execution is unavailable is infrastructure/tooling access rather than a known failing test;
- relevant prior machine evidence exists for the architectural claim being promoted;
- the unexecuted delta is independently source-reviewed and all blocking review findings are resolved;
- targeted regression tests or equivalent falsifiers are added for material defects discovered in review;
- the promotion record labels the delta `not_run` or equivalent and never claims it passed;
- production or executable-substrate reliance is prohibited until the next available local validation gate passes;
- the next gate, owner, command, and failure response are explicit.

This exception is intentionally narrow. It may move a governed architecture decision forward without buying hosted CI, but it may not turn unexecuted code into accepted production substrate.

## GitHub Actions posture

Repository workflows are retained as reproducible recipes and optional manual replication surfaces. Automatic pull-request and push triggers are disabled while hosted Actions capacity is not part of the operating model.

A maintainer may manually invoke a workflow later if hosted capacity becomes available. No project gate should require that invocation unless the gate is explicitly revised by human decision.

## Failure semantics

| State | Meaning | Gate effect |
|---|---|---|
| `passed` | command executed and acceptance checks passed | satisfies its validation class |
| `failed` | command executed and acceptance checks failed | blocks affected promotion |
| `hosted_ci_unavailable` | hosted executor did not run because capacity/service was unavailable | non-blocking; use local route |
| `not_run` | validation has not yet been executed | cannot be claimed as passed; may use the narrow explicit exception above |
| `not_applicable` | validation class does not apply to the change | non-blocking with rationale |
| `carried_forward` | prior evidence remains relevant to unchanged behavior | usable only within its original scope |
| `exception_promoted` | narrow governed exception used for a non-production/reversible decision | must carry a mandatory next executable gate |

## Review and revisit triggers

Revisit this policy if:

- branch protection introduces a required hosted status check;
- a local and hosted run disagree materially;
- local validation is found to omit a gate previously enforced by CI;
- a security or release requirement genuinely needs an isolated external executor;
- the project adopts another no-cost or self-hosted validation runtime;
- execution exceptions become routine rather than rare, bounded, and explicitly justified.

The preferred response to those events is to restore the missing validation capability without making paid hosted CI a product-development dependency.
