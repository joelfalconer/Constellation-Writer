# F1 Architecture Coherent Readiness v0.2

## Current readiness

```yaml
status: conditional_not_ready
contract_kernel: implemented_candidate
reference_fixture: expanded_and_machine_checked
validator: v0_2_tested_in_github_actions
negative_tests: tested_in_ci
technology_adrs: proposed_pending_spikes
vertical_slice: routed_issue_6_not_executed
human_review: pending
research_evidence: materialized_candidate_exact_locators_partial
```

## Machine evidence now available

GitHub Actions run `30344185332` completed successfully at head `6b48da2d5e90003052111feadea5dfa26d17d268`. The preserved validation artifact reports validator v0.2 passed with 22 schemas, 3 Sheets, 2 manuscripts, and zero issues.

This closes the previous uncertainty about whether the committed validator and negative contract tests run successfully in CI. It does not test desktop behavior or service implementations.

## Remaining blockers

- Human-review Product Constitution, authority matrices, typed UUIDv7 direction, annotation separation, and Compendium deferral.
- Execute Tauri vs Electron shell spike #3.
- Execute CodeMirror prose/accessibility spike #4.
- Execute Workbench compile-plan/Pandoc adapter spike #5.
- Execute durable substrate vertical slice #6.
- Backfill exact source locators for Deep Research evidence units before claiming strong evidence traceability.

## F1 entry criteria

| Criterion | State |
|---|---|
| candidate schemas and fixture pass CI | pass at recorded head |
| negative duplicate/missing-reference controls execute | pass through CI test suite |
| deliverables register matches repository | updated in v0.4.0 |
| critical architecture contradictions have routes | pass candidate |
| technology spike plans have acceptance measures | pass, issues #3-#5 |
| human architecture review | open |

## F1 closure criteria

F1 may close only when:

- one canonical owner exists for every v1 durable field;
- foundation schemas and fixtures remain machine checked at the promotion head;
- architectural rivals are either tested or explicitly deferred with accepted risk;
- technology spike decisions are recorded in ADRs;
- the executable substrate exposes no architecture-breaking contradiction;
- human approval is recorded in a gate receipt.

## Route

The document and contract build-out is no longer the F1 bottleneck. The route is now empirical: technology spikes, vertical-slice behavior, fault injection, and human gate review.
