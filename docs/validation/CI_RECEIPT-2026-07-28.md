# CI Validation Receipt: Foundation Contracts

```yaml
run_id: 30344185332
workflow: Validate foundation contracts
head_sha: 6b48da2d5e90003052111feadea5dfa26d17d268
branch: foundation/project-establishment
event: pull_request
status: completed
conclusion: success
validation_state: tested
artifact_id: 8682213890
artifact_name: foundation-validation-report
artifact_digest: sha256:ab1aae365d440c311bbcd1c3629efb55ee0f67a37e2d1700ae21054aec98e70b
```

## Validation report

The preserved workflow artifact reports:

```json
{
  "validator_version": "0.2.0",
  "status": "passed",
  "issues": [],
  "counts": {
    "schemas": 22,
    "sheets": 3,
    "manuscripts": 2,
    "issues": 0
  }
}
```

## Interpretation

This is machine evidence that the current contract and reference-fixture checks passed the committed validator and negative contract test workflow at the stated SHA. It is **not** evidence that compile, recovery, editor, or mutation services work, because those services have not yet been implemented and exercised.
