# Contributing

Constellation Writer is in governed foundation development.

## Before changing architecture or contracts

- read the Product Constitution, Canonicality Matrix, Invariant Registry, and relevant ADRs;
- identify the canonical state affected;
- explain migration and reversal cost;
- update schemas, fixtures, validator, and documentation together;
- do not promote candidate material without the required gate evidence.

## Pull requests

A PR should include:

- intent and scope;
- affected invariants and ADRs;
- canonical and derived state changes;
- tests and validation results;
- privacy and recovery implications;
- rollback or deprecation path;
- unresolved risks.

## Repository safety

Never commit secrets, private manuscripts, identifying user research data, copyrighted corpora without permission, or font binaries. Use synthetic fixtures.
