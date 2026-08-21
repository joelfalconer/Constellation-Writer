# F1 Architecture Coherent Entry Receipt

Date: 2026-08-17
Repository: `joelfalconer/Constellation-Writer`
Transition: F0 accepted → F1 entry
Status: **conditional_not_ready**

## Compact Run Contract

```yaml
project_descriptor: Constellation Writer local-first professional writing workbench
decision_context: reconcile canonical state after F0 promotion and establish an honest F1 entry baseline
primary_outcomes:
  - record F0 acceptance against the actual merge and CI evidence
  - remove stale F0-pending language from operational state
  - preserve and route every real F1 blocker
research_corpus:
  - main branch at foundation merge 1f01da3c76611d9ad9b1b297c2b8f265a91a6daa
  - foundation validator and contract tests
  - Product Constitution, canonicality/authority/invariant/dependency contracts
  - ADR registry and contradiction register
  - issues 2, 3, 4, 5, 7
constraints:
  - do not reinterpret F0 acceptance as F1 acceptance
  - do not promote technology ADRs without spike evidence
  - do not treat F2 vertical-slice execution as already completed
  - preserve unresolved evidence gaps and critical contradictions
acceptance_tests:
  - main merge verified
  - clean main CI verified
  - F0 acceptance receipt present
  - state/gate/delivery records reconciled
  - every F1 blocker has owner, issue or explicit record, acceptance condition, and revisit trigger
destination: F1 evidence acquisition and architecture gate review
```

## Verified baseline

- Foundation PR #1 is merged to `main` at `1f01da3c76611d9ad9b1b297c2b8f265a91a6daa`.
- The accepted foundation head had already passed CI before merge.
- A clean GitHub Actions checkout of the merge commit passed run `32010291279`.
- The preserved validator artifact reports 22 schemas, 3 Sheets, 2 manuscripts, and zero issues.
- The current validator reports no modeled canonical-authority drift.

## F1 blockers retained

| Blocker | Owner | Acceptance condition | Revisit trigger |
|---|---|---|---|
| #3 Tauri 2 vs Electron shell | `joelfalconer` | equivalent bounded shells measured; ADR-0004 accepted/rejected/deferred from evidence | before desktop application scaffold is accepted |
| #4 CodeMirror 6 vs serious prose rival | `joelfalconer` | longform, IME, bidi, accessibility, selection and latency evidence; ADR-0005 decision | before editor package architecture is accepted |
| #5 Workbench AST + Pandoc boundary | `joelfalconer` | deterministic compile-plan/golden/source-map evidence; ADR-0006 decision | before P2 Manuscript Machine implementation |
| #7 evidence lineage refresh | `joelfalconer` | EU-001–010 locators resolved or explicitly justified; current benchmark claims sourced | before F1 human gate review or benchmark-completeness claims |
| CON-003 mutation ownership | architecture gate | shared Mutation Envelope boundary survives cross-spec/adversarial review | F1 closure, and again if F2 implementation creates competing transaction ownership |

## Sequencing reconciliation

Earlier foundation prose treated durable substrate vertical slice #6 as an F1 blocker. The accepted roadmap execution sequence now places **F1 Architecture Coherent closure before F2 durable substrate vertical slice #6**. Therefore #6 is a downstream F2 execution gate and later architecture falsifier, not a prerequisite for entering or closing F1 unless the F1 review explicitly requests a bounded implementation probe.

This change is sequencing clarification, not evidence that the substrate works.

## Decision

F1 entry is valid. F1 closure is not.

The next work is empirical and adversarial: #7 and spikes #3–#5 may proceed, then the F1 closure run must adjudicate ADRs, authority boundaries, critical contradictions, and residual risks. If F1 passes, route directly to #6.

## Epistemic annotation

```yaml
epistemic_basis: derived_result
work_function: decision
validation_state: human_reviewed_and_machine_checked_baseline
```

## Outcome observation contract

Observe at the next F1 review:

- whether each blocker produced reproducible evidence;
- whether any candidate ADR was falsified;
- whether canonical ownership or lifecycle drift emerged;
- whether CON-003 can be resolved without hidden transaction duplication;
- whether the gate should pass, fail, or route targeted remediation.
