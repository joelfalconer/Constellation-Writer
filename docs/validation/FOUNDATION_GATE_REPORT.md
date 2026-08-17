# Foundation Gate Report v0.2

## Decision summary

**F0 Project Defined:** candidate package complete, awaiting explicit human acceptance.  
**F1 Architecture Coherent:** conditional, not closed. Machine contract validation now passes; technology and executable behavior remain open.

## Evidence available

- Programme definition, user/non-user profiles, scope, success definition, deliverables, and routing.
- Product Constitution, sovereignty, canonicality, authority, dependency, trust, anti-feature, and reversal-cost laws.
- Integrated component specifications and shared contract kernel.
- Research evidence ledger, source decisions, feature atomicity, switching/friction maps, benchmark dossier candidates, and coverage report.
- Expanded reference novel, deterministic validator, and negative controls.
- GitHub Actions validation receipt with successful v0.2 report.
- Product experience contracts and writer journey maps.
- Prototype stress, performance, recovery, privacy, accessibility, external-editor, compile-golden, and failure-injection test definitions.
- Candidate technology ADRs with routed spikes.

## F0 gates

| Criterion | State |
|---|---|
| project identity clear | candidate pass |
| intended users and deliberate non-fit defined | candidate pass |
| v1 scope and non-goals explicit | candidate pass |
| authority hierarchy defined | candidate pass |
| deliverables mapped and materialized | candidate pass |
| success criteria testable | candidate pass |
| backlog, milestones, owners/routes exist | candidate pass |
| human acceptance | **open** |

## F1 gates

| Criterion | State |
|---|---|
| modeled durable fields have explicit authorities | candidate pass |
| shared enums and lifecycles reconciled | machine checked where schema/validator covers them |
| reference fixture validates | pass at CI run 30344185332 |
| negative fixtures fail for expected reasons | pass in committed CI test suite |
| cache deletion leaves canonical validation unchanged | contract invariant, executable service test open |
| compile semantics deterministic | test definitions exist, implementation open |
| mutation and recovery ownership unified | candidate pass through Mutation Envelope |
| desktop/editor/compile technology rivals tested | open issues #3-#5 |
| durable substrate vertical slice | open issue #6 |
| human architecture approval | open |

## Exceptions and unresolved material

- Deep Research evidence entries still require exact source-locator backfill.
- Benchmark dossiers preserve current evidence limits and are not fresh product audits.
- No desktop prototype has passed the long-session assay.
- No recovery implementation has passed failure injection.
- No technology ADR is accepted.
- Main remains intentionally unpromoted until the gate decision.

## Route

1. Human-review F0 constitutional artifacts and record accept/revise decision.
2. Execute technology spikes #3-#5 and update ADRs.
3. Execute vertical slice #6 and populate its reserved receipt.
4. Run fault injection and compile goldens against real services.
5. Review F1 with machine evidence and human decision.

## Promotion rule

Documentation completeness is not architecture validation. Do not merge or close F1 until the relevant machine evidence and human decisions exist.
