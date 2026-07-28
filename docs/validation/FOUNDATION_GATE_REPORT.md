# Foundation Gate Report v0.1

## Decision summary

**F0 Project Defined:** materially complete as a candidate, pending human acceptance.  
**F1 Architecture Coherent:** not yet closed. Contract and validator machinery exist, but CI and executable product behavior remain unproven.

## Evidence available

- Product thesis, vision, users, anti-personas, scope, and success definition.
- Product Constitution, sovereignty, canonicality, authority, dependency, trust, and anti-feature laws.
- Integrated component specifications and common contract kernel.
- Typed identifier, revision, anchor, provenance, lifecycle, consequence, validation, and recovery schemas.
- Expanded reference novel and deterministic validator.
- Validation assays, performance budget, recovery drills, and adversarial review.
- Candidate technology ADRs.

## F0 gates

| Criterion | State |
|---|---|
| project identity clear | candidate pass |
| intended users and non-users defined | candidate pass |
| v1 scope and non-goals explicit | candidate pass |
| authority hierarchy defined | candidate pass |
| deliverables mapped | candidate pass |
| success criteria testable | candidate pass |
| backlog and next route exist | candidate pass |
| human acceptance | open |

## F1 gates

| Criterion | State |
|---|---|
| every modeled durable field has one owner | candidate, validator partial |
| shared enums and lifecycles reconciled | candidate |
| reference fixture validates | prior local v0.1 validator pass; v0.2 CI pending |
| invalid fixtures fail for expected reasons | tests added, execution pending |
| cache deletion leaves canonical validation unchanged | specified, not executable product test |
| compile semantics deterministic | specified, not implemented |
| mutation and recovery ownership unified | candidate pass |
| technology spikes completed | open |

## Exceptions

- Original research evidence units are not fully atomized.
- Current schemas cover the foundation fixture, not every future field.
- No desktop prototype has passed the workflow assay.
- No recovery implementation has passed fault injection.
- No technology ADR is accepted.

## Route

1. Run GitHub CI and repair contract/test failures.
2. Review and accept or revise F0 constitutional artifacts.
3. Build technology spikes.
4. Implement the first vertical slice.
5. Run F1 machine and human gate review.

## Promotion rule

Do not merge or label F1 accepted solely because the documentation is comprehensive. F1 requires machine evidence and a recorded human decision.
