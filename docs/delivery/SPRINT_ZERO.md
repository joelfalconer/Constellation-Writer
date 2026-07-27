# Sprint Zero: Foundation Contracts and Validator

## Objective

Turn the repository foundation into a mechanically checkable architecture package.

## Deliverables

- Accepted or revised Product Constitution.
- Accepted canonicality and state-authority matrices.
- Completed common schema kernel.
- State-machine registry.
- Validator CLI skeleton.
- Reference fixture validation command.
- Cross-spec contradiction and enum drift report.
- Technology decision briefs for desktop shell and editor engine.
- Prototype Stress Assay draft.

## Work sequence

1. Review PR #1 constitution and scope.
2. Resolve identifiers, annotation storage, and mutation ownership.
3. Complete common schemas and registries.
4. Add deterministic schema checks.
5. Expand fixture and run validation.
6. Emit F0 receipt and F1 readiness report.

## Acceptance

- All JSON and YAML candidate contracts parse.
- Fixture IDs are unique and references resolve.
- Every canonical field in current schemas maps to one authority.
- Deleting fixture `.workbench/` has no effect on canonical validation.
- Open contradictions have owners or explicit revisit triggers.
