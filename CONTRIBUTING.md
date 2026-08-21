# Contributing

Constellation Writer is in governed foundation development.

## Before changing architecture or contracts

- read the Product Constitution, Canonicality Matrix, Invariant Registry, and relevant ADRs;
- identify the canonical state affected;
- explain migration and reversal cost;
- update schemas, fixtures, validator, and documentation together;
- do not promote candidate material without the required gate evidence.

## Validation

Hosted GitHub Actions is an optional replication surface, not a project gate. The default deterministic validation path is local:

```bash
python -m pip install -r tools/validator/requirements.txt
python tools/local_validate.py --suite all
```

The runner emits `build/local-validation-receipt.json`. Treat an unavailable hosted runner or exhausted Actions quota as infrastructure unavailability, not as a failed test. An actually executed failing test remains blocking.

See `docs/validation/LOCAL_VALIDATION_POLICY.md` for evidence classes, promotion rules, and the distinction between local deterministic checks, hosted cross-platform replication, and physical/human assays.

## Pull requests

A PR should include:

- intent and scope;
- affected invariants and ADRs;
- canonical and derived state changes;
- tests and validation results;
- privacy and recovery implications;
- rollback or deprecation path;
- unresolved risks.

If hosted CI did not run, record the local validation receipt or explicitly mark validation as `not_run`; never report quota exhaustion as a code failure.

## Repository safety

Never commit secrets, private manuscripts, identifying user research data, copyrighted corpora without permission, or font binaries. Use synthetic fixtures.
