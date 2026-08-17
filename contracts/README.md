# Contract Kernel

This directory contains machine-readable schemas shared by all domain specifications.

Rules:

1. Component schemas import common definitions rather than cloning them.
2. The common kernel owns identity, revision, anchors, provenance, lifecycle, consequence, validation, and errors.
3. Schema examples are candidates until validated by the contract test suite.
4. Generated language bindings are derived artifacts.
