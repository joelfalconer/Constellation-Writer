# Release and Versioning Policy v0.1

## Independent versions

Constellation Writer versions:

- application runtime;
- project-vault schema;
- component contracts;
- compile profile/schema;
- validator;
- publication artifacts.

These versions must not be collapsed into one number.

## Status ladder

```text
planned → draft → candidate → machine_checked → human_reviewed → tested → accepted
                                      ↘ contradicted / superseded / deprecated
```

## Candidate releases

Foundation tags may use:

```text
foundation-v0.2.0-candidate
```

A candidate tag means a reproducible review point, not production readiness.

## Application releases

- Semantic versioning after the first public alpha.
- Every release records compatible vault schema range.
- Breaking vault migration requires pre-migration snapshot and tested rollback.
- Compile adapter/version changes require golden-output comparison.

## Release contents

- changelog;
- signed or checksummed application artifacts where available;
- schema and migration manifest;
- validation report;
- known limitations;
- rollback instructions;
- privacy/security notes.

## Promotion gates

- no failing required CI;
- gate receipt matches claimed status;
- critical risks either closed or explicitly accepted;
- recovery path tested for migration-bearing releases;
- no private corpora, secrets, or unlicensed font binaries.
